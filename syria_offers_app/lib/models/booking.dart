class Booking {
  final String userName;
  final String userPhone;
  final DateTime bookedAt;
  final int quantity;
  final double totalPrice;
  final int offerId;

  Booking({
    required this.userName,
    required this.userPhone,
    required this.bookedAt,
    required this.quantity,
    required this.totalPrice,
    required this.offerId,
  });
}