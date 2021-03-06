# Changelog

All notable changes to this project will be documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
The project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased
- **/admin** endpoint
  - Django Admin interface is configured and tested
  - supports filtering, "View in API" & term-selection widgets
- **/login** endpoint: user login (Token authentication)
- ALL model endpoints
  - authentication: only users can create/update new database objects.
  - all fields are documented (with 'help_text')
- **/api/userprofile** endpoint: user profiles (UserProfile model)
  - custom user model (uses email for authentication rather than username).
  - fields: firstname, lastname, email, orcidid, homepage
  - email validation: uniqueness
  - orcidid validation: syntax, uniqueness
  - supports creation of normal and super-users.
  - supports search/filtering (by firstname, lastname, email, orcidid)
  - topic validation:  TO DOCUMENT
- **/news** endpoint: user news items (NewsItem model)
  - fields: user profile (id), news_text, created_on
  - authentication: users can only update/delete their own news items.
  - a user's news items are deleted if their profile is deleted.
- **/event** endpoint: events (Event model)
  - fields: user profile (id), ...
  - a user's events are preserved if their profile is deleted.
- **/eventkeyword** endpoint: event keywords (EventKeyword model)
- **/eventprerequisite** endpoint: event prerequisites (EventPrerequisite model)
  - fields: event, keyword|prerequisite
  - the endpoint allows registration of keywords|prerequisites independent of an event
  - (useful for pre-population of common keywords|prerequisites)
  - any user can create a keyword|prerequisite, but only superuser can update or delete
  - keywords|prerequisites must be unique

### Added
### Changed
### Removed
### Fixed
