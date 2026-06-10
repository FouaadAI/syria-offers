# Standard Prompt Templates

Copy and paste these templates when assigning tasks to ensure the AI follows all project rules (Architecture, Localization, Widgets).

---

## **1. Create New Page (Tạo màn hình mới)**

Use this prompt to trigger the **7-Step UI Workflow**:

```text
Create a new page:
- **Feature Name**: [e.g. work_report]
- **Route Type**: [Fullscreen (AppPages) OR Nested (HomeRouter/CustomerRouter) OR Common (CommonRouter)]
- **Key UI Components**: [List existing widgets or describe new ones, e.g. AppInput, DatePicker]
- **Logic**: [Brief description of what the page does]
```

**What the AI will do:**
1.  Scaffold `lib/src/ui/work_report/{binding,interactor,components}`.
2.  Create `LocaleKey` & update `lang_*.dart` (Localization).
3.  Implement UI using `App*` widgets & `AppColors`.
4.  Register the route in the correct file (`app_pages.dart` or `*_router.dart` or `common_router.dart`).

---

## **2. Create New Widget (Tạo Widget chung)**

Use this when you need a reusable component in `lib/src/ui/widgets/`:

```text
Create a shared widget:
- **Name**: App[Name] (e.g. AppRatingBar)
- **Usage**: [Where will it be used?]
- **Style**: [Reference AppColors/AppStyles]
```

**What the AI will do:**
1.  Create `lib/src/ui/widgets/app_[name].dart`.
2.  Use `StatelessWidget` and `const` constructor.
3.  Apply `AppColors`/`AppStyles`.

---

## **3. Refactor UI (Clean Code)**

Use this when a file is getting too long:

```text
Refactor this page: [Path to file]
- Extract sub-widgets to `components/` folder.
- Replace raw widgets with `App*` widgets.
- Fix hardcoded strings/colors.
```

---

## **4. Finalize Feature (Commit + Push + PR)**

Use this after completing UI/API work to trigger CI/CD rule and PR creation:

```text
Finalize this feature:
- Branch name: [e.g. feat/login-session-timeout]
- Commit message: [e.g. feat(auth): handle session timeout]
- Commit now?: [yes/no]
- Push now?: [yes/no]
- Create PR now?: [yes/no]
- Base branch: [e.g. dev]
- PR title: [e.g. feat(auth): handle session timeout]
- Feature summary: [...]
- UI summary: [...]
- Reviewer notes: [...]
- Screenshot evidence: [No UI OR before/after]
- Paired with: [Solo OR name]
```

---

## **5. Refactor Converted UI (Post-Convert)**

Use this when code comes from convert script and needs production refactor:

```text
Refactor converted UI:
- Source file: [e.g. lib/src/ui/home_demo_figma/home_demo_figma_page.dart]
- Feature name: [e.g. home_demo]
- Keep exact Figma visual: [yes/no]
- Needs API integration now?: [yes/no]
- MCP assets json path: [e.g. spec/figma-assets/home_demo-mcp-assets.json]
- Normalize/rename convert assets?: [yes/no]
- Commit now?: [yes/no]
- Push now?: [yes/no]
- Create PR now?: [yes/no]
- Priority fixes: [naming, localization, App* widgets, token cleanup, asset-rename, overflow]
```

Expected behavior:
1. Apply `ui-refactor-convert.md` + `ui.md`.
2. Rename generated classes/files to semantic names.
3. If MCP is used, download assets via `node tool/download_figma_mcp_assets.mjs ...` first.
4. Normalize convert-generated asset folder and names, then update `AppAssets` usages.
5. Replace hardcoded style/string with tokens + localization.
6. Extract components and pass UI correctness gates.
7. Ask and execute in order: commit -> push -> create PR.
