# Changelog

## Unreleased

### Added

- play_time, product_id to `library.models`
- Tag class to `library.models`
- app_context, lutris to `extensions`
- count_tags, count_platforms, total_playtime functions to `extensions.utils`
- Game search function
- Platform vector images
- Sidebar modules to Library UI
- Settings form
- Markdown support for descripton, note fields
- game_tags, platform_tags to template_tags
- Export functions for Lutris, Steam
- Recently Modified sidebar module
- scan_games, get_lutris_data, get_steam_data to `extensions.utils`

### Changed

- Migrated from Flask to Django
- steam_id to game_id in `library.models`
- last_played field from datetime to int in `library.models`
- Added query support for pagination
- Updated Library UI
- Reconfigured system directory settings


## [0.0.0] - 2024.0309

### Added

- Changelog, documentation, Pipfiles
- Main and Config modules
