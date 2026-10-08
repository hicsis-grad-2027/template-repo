# Frontend: the part users see

The mobile app or website your users open. If the project has both (e.g. a customer app and an admin website), rename this folder to `mobile/` and add a `web/` folder, each with its own README like this one.

**بالعربي:** ده الجزء اللي المستخدم بيشوفه: تطبيق موبايل أو موقع. لو المشروع فيه الاتنين، سمّوا الفولدر ده `mobile/` واعملوا فولدر `web/` جنبه.

## Start here (first time only)

Create the project inside this folder. Pick the one that fits:

```bash
cd frontend

# Flutter app
flutter create --org com.yourteam --project-name your_app .

# or a web app (React example)
npm create vite@latest . -- --template react-ts
```

If the tool replaces this README, get it back with `git checkout frontend/README.md`.

## Every day

| Flutter | Web |
|---|---|
| `flutter pub get` | `npm install` |
| `flutter run` | `npm run dev` |
| `dart format .` | `npm run lint` |
| `flutter analyze` | `npm run build` |
| `flutter test` | `npm test` |

These are the same checks CI runs on your pull request (it finds `pubspec.yaml` or `package.json` by itself), so run them before you push.

## Rules for this folder

- **No hardcoded API address.** Read it from config (`--dart-define` in Flutter, an env variable on the web).
- **Keep the layers apart.** Screens/components show data. One `services/` (or `api/`) folder calls the backend. Business rules live in the backend.
- **Every screen has three states:** loading, empty, and error with a clear message.
- **If the app is in Arabic,** set right-to-left from the first screen, not at the end.
- **No keys in the app or in git.** Anything secret belongs on the backend.

## Read also

- [How we work](../docs/01-workflow.md): issue → branch → pull request
- [Engineering principles](../backend/PRINCIPLES.md): written for the backend, but the same five habits apply here
