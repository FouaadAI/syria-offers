# Design System (Syria Offers App)

## Core Tokens

- `primary`: `Theme.of(context).colorScheme.primary`  
  Main brand blue for AppBar, primary actions, active states.
- `secondary`: `Theme.of(context).colorScheme.secondary`  
  Accent orange for important highlights and CTAs.
- `surface/card`: `Theme.of(context).cardTheme.color` / `Theme.of(context).colorScheme.surface`  
  Card and panel backgrounds.
- `scaffold background`: `Theme.of(context).scaffoldBackgroundColor`  
  Global page background.
- `onPrimary`: `Theme.of(context).colorScheme.onPrimary`  
  Text/icons on primary-colored elements.

## Typography

- Primary reading font (Arabic-first): `Cairo` via app `textTheme`.
- Secondary Latin/numeric support: `Inter` mapped into label/body variants in theme.
- Avoid per-widget hardcoded fonts unless there is a strict visual requirement.

## Components

- **AppBar**: flat (`elevation: 0`), primary background, centered white title.
- **Card**: white surface, radius ~14, soft elevation (2–4), minimal borders.
- **ElevatedButton**: primary background, white text, radius ~10, comfortable padding.
- **Input fields**: filled white, rounded border (~8), primary focus border.
- **Lists/Tiles**: prefer theme colors and typography; avoid inline brand colors.

## Usage Rules

1. Prefer theme tokens over hardcoded colors.
2. Use `primary` for default actions/navigation emphasis.
3. Use `secondary` for accent/attention actions (price highlight, key CTA).
4. Keep neutral grays only for placeholders, disabled states, and subtle separators.
5. Preserve RTL-friendly spacing and `EdgeInsetsDirectional` where applicable.
