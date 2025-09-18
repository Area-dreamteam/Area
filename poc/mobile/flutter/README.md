# Flutter POC
## Only front-end with a Login and Register Page

### Objective

- A simple login and register form
- No back-end connection and no database, API
- Basic page redirection with the path of the page when the user submit
- And a final page with Connect or Registed

### Prerequisites
- Flutter SDK installed (`flutter --version` to verify)


### Installation and Run

``` bash

# Fetch dependencies
flutter pub get

# Run on a connected device or emulator
flutter run
```

### Project Structure
```
tree -L 3 -I "android|ios|linux|macos|windows|web|build|.git|test|pubspec.lock|*.iml|analysis_options.yaml"

.
├── lib/
│   ├── main.dart                  # App entry (routes/navigation)
│   └── screens/
│       ├── login.dart             # Login form -> navigates to "Logged" confirmation
│       ├── register.dart          # Register form -> navigates to "Registered" confirmation
│       └── widgets/               # Reusable UI widgets (inputs, buttons, etc.)
├── pubspec.yaml                   # Dependencies & assets
└── README.md
```