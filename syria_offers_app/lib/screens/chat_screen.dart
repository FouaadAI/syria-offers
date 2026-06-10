import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:provider/provider.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:http/http.dart' as http;
import 'package:open_filex/open_filex.dart';
import 'package:path_provider/path_provider.dart';
import 'package:syria_offers_app/services/api_service.dart';
import 'package:syria_offers_app/models/offer.dart';
import 'package:syria_offers_app/config.dart';
import 'package:syria_offers_app/localization/app_localizations.dart';
import 'package:syria_offers_app/screens/offer_detail_screen.dart';

class ChatScreen extends StatefulWidget {
  const ChatScreen({super.key});

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final TextEditingController _controller = TextEditingController();
  final List<ChatMessage> _messages = [];
  final ScrollController _scrollController = ScrollController();
  bool _isLoading = false;
  String _sessionId = '';
  bool _initialized = false;

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    if (!_initialized) {
      _initialized = true;
      final loc = AppLocalizations.of(context);
      _messages.add(ChatMessage(
        text: loc.greetingMessage!,
        isUser: false,
      ),);
    }
  }

  void _scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  void _sendMessage() async {
    if (_controller.text.trim().isEmpty || _isLoading) return;

    final userMessage = _controller.text.trim();
    setState(() {
      _messages.add(ChatMessage(text: userMessage, isUser: true));
      _controller.clear();
      _isLoading = true;
    });
    _scrollToBottom();

    try {
      final apiService = Provider.of<ApiService>(context, listen: false);
      final result = await apiService.chatQuery(userMessage, sessionId: _sessionId);

      setState(() {
        if (result['session_id'] != null && (result['session_id'] as String).isNotEmpty) {
          _sessionId = result['session_id'] as String;
        }

        final offersJson = result['offers'] as List;
        final planId = result['plan_id'] as int?;

        if (offersJson.isNotEmpty) {
          final offers = offersJson.map((json) => Offer.fromJson(json)).toList();
          _messages.add(ChatMessage(
            text: result['reply'] ?? 'Offer found',
            isUser: false, offers: offers,
          ),);
        } else if (planId != null) {
          _messages.add(ChatMessage(
            text: result['reply'] ?? 'Plan created.',
            isUser: false, planId: planId,
          ),);
        } else {
          _messages.add(ChatMessage(
            text: result['reply'] ?? 'No results found.',
            isUser: false,
          ),);
        }
        _isLoading = false;
        _scrollToBottom();
      });
    } catch (e) {
      setState(() {
        _messages.add(const ChatMessage(text: '⚠️ Error. Try again.', isUser: false));
        _isLoading = false;
        _scrollToBottom();
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final loc = AppLocalizations.of(context);
    return Scaffold(
      appBar: AppBar(title: Text(loc.chatTitle!)),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              controller: _scrollController,
              padding: const EdgeInsets.all(12),
              itemCount: _messages.length,
              itemBuilder: (context, index) => _buildMessageBubble(_messages[index]),
            ),
          ),
          if (_isLoading)
            const Padding(
              padding: EdgeInsets.all(8.0),
              child: LinearProgressIndicator(),
            ),
          SafeArea(
            child: Padding(
              padding: const EdgeInsets.all(8.0),
              child: Row(
                children: [
                  Expanded(
                    child: TextField(
                      controller: _controller,
                      maxLines: 5,
                      minLines: 1,
                      keyboardType: TextInputType.multiline,
                      textInputAction: TextInputAction.newline,
                      decoration: InputDecoration(
                        hintText: loc.chatHint!,
                        border: OutlineInputBorder(borderRadius: BorderRadius.circular(24)),
                      ),
                    ),
                  ),
                  const SizedBox(width: 8),
                  CircleAvatar(
                    backgroundColor: Theme.of(context).colorScheme.primary,
                    child: IconButton(
                      icon: Icon(Icons.send, color: Theme.of(context).colorScheme.onPrimary),
                      onPressed: _isLoading ? null : _sendMessage,
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildMessageBubble(ChatMessage msg) {
    final loc = AppLocalizations.of(context);
    return Align(
      alignment: msg.isUser ? Alignment.centerRight : Alignment.centerLeft,
      child: GestureDetector(
        onLongPress: () {
          Clipboard.setData(ClipboardData(text: msg.text));
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text(loc.copyText!)),
          );
        },
        child: Container(
          margin: const EdgeInsets.symmetric(vertical: 4),
          padding: const EdgeInsets.all(12),
          constraints: BoxConstraints(maxWidth: MediaQuery.of(context).size.width * 0.8),
          decoration: BoxDecoration(
            color: msg.isUser
                ? Theme.of(context).colorScheme.primary.withValues(alpha: 0.12)
                : Colors.white,
            borderRadius: BorderRadius.circular(14),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(msg.text),
              if (msg.offers != null && msg.offers!.isNotEmpty) ...[
                const SizedBox(height: 8),
                ...msg.offers!.map((offer) => Card(
                      margin: const EdgeInsets.only(bottom: 4),
                      child: ListTile(
                        title: Text(offer.titleAr, style: const TextStyle(fontSize: 14)),
                        subtitle: Text('${offer.offerPrice.toStringAsFixed(0)} ${loc.price}'),
                        trailing: const Icon(Icons.arrow_forward_ios, size: 16),
                        onTap: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(builder: (_) => OfferDetailScreen(offer: offer)),
                          );
                        },
                      ),
                    ),),
              ],
              if (msg.planId != null) ...[
                const SizedBox(height: 8),
                ElevatedButton.icon(
                  onPressed: () => _exportToCalendar(msg.planId!),
                  icon: const Icon(Icons.calendar_today),
                  label: Text(loc.exportCalendar!),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Theme.of(context).colorScheme.secondary,
                    foregroundColor: Theme.of(context).colorScheme.onSecondary,
                  ),
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }

  Future<void> _exportToCalendar(int planId) async {
    final loc = AppLocalizations.of(context);
    final icsUrl = '${AppConfig.baseUrl}/travel-planner/$planId/export-ics';

    try {
      // 1. ICS-Datei herunterladen
      final response = await http.get(Uri.parse(icsUrl));
      if (response.statusCode != 200) throw Exception('Download failed');

      // 2. In temporärem Ordner speichern
      final dir = await getTemporaryDirectory();
      final file = File('${dir.path}/travel_plan_$planId.ics');
      await file.writeAsBytes(response.bodyBytes);

      // 3. Mit open_filex öffnen → System wählt Kalender-App aus
      final result = await OpenFilex.open(file.path, type: 'text/calendar');

      if (result.type != ResultType.done) {
        // Fallback: URL im Browser öffnen
        throw Exception('Could not open file');
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(loc.calendarFailed!),
            action: SnackBarAction(
              label: loc.download!,
              onPressed: () => launchUrl(Uri.parse(icsUrl), mode: LaunchMode.externalApplication),
            ),
          ),
        );
      }
    }
  }
}

class ChatMessage {
  final String text;
  final bool isUser;
  final List<Offer>? offers;
  final int? planId;

  const ChatMessage({
    required this.text,
    required this.isUser,
    this.offers,
    this.planId,
  });
}