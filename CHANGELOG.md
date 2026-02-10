# Changelog

All notable changes to this project are documented in this file.

## [v2.0.0] - 2026-02-10
- Removed the weather feature and associated API usage to focus on wellness and moderation.
- Expanded wellness content:
  - Larger, more diverse set of motivational quotes and affirmations.
  - More workout ideas, short circuits, and desk-friendly stretches.
  - Additional breathing exercises including Alternate Nostril and energizing patterns.
  - Expanded wellness tips with habit-focused suggestions.
- Water reminders: expanded the set of reminder phrases and improved messaging.
- Added two moderator commands: `purge` (bulk-delete messages) and `announce` (post announcement embeds).
- Updated help/about text, README, and man page to reflect the new focus.
- Removed `requests` from runtime requirements.

## [v1.0.5] - 2026-02-08
- Maintenance release with quality-of-life improvements and bug fixes.
- Fixes and improvements:
  - Improved DM handling and attachment relay for the `dm` command.
  - Hardened reminder delivery logic to reduce lost reminders across restarts.
  - Improved help text and command descriptions for clarity.
  - Minor stability and permission handling fixes for guild interactions.

## [v1.0.0] - Initial release
- Core features: weather queries, motivational quotes, hydration reminders, workouts, breathing exercises, tips, dice rolling, reminders, and basic info commands.
