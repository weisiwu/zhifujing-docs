# poetry-app（诗词应用）

> This is an [Expo](https://expo.dev) project created with [`create-expo-app`](https://www.npmjs.com/package/create-expo-app).

## 技术栈

| 类别 | 技术 |
|------|------|
| 框架 | Expo ~54.0.0 |
| 语言 | React 19.1.0 |
| 语言 | TypeScript |
| UI | react-native-paper |
| 状态管理 | Zustand |
| 后端 | Supabase |
| 本地存储 | better-sqlite3 |

## 关键依赖

| 包名 | 版本 |
|------|------|
| `@aws-amplify/ui-react` | ^6.15.1 |
| `@expo/vector-icons` | ^15.0.3 |
| `@react-native-async-storage/async-storage` | ^2.2.0 |
| `@react-navigation/bottom-tabs` | ^7.15.3 |
| `@react-navigation/elements` | ^2.6.3 |
| `@react-navigation/native` | ^7.1.31 |
| `@supabase/supabase-js` | ^2.98.0 |
| `better-sqlite3` | ^12.8.0 |
| `expo` | ~54.0.0 |
| `expo-build-properties` | ~1.0.10 |
| `expo-constants` | ~18.0.13 |
| `expo-device` | ^55.0.9 |
| `expo-font` | ~14.0.11 |
| `expo-haptics` | ~15.0.8 |
| `expo-image` | ~3.0.11 |
| `expo-linking` | ~8.0.11 |
| `expo-modules-core` | ~3.0.0 |
| `expo-notifications` | ^55.0.12 |
| `expo-router` | ~6.0.23 |
| `expo-splash-screen` | ~31.0.13 |
| `expo-status-bar` | ~3.0.9 |
| `expo-symbols` | ~1.0.8 |
| `expo-system-ui` | ~6.0.9 |
| `expo-web-browser` | ~15.0.10 |
| `react` | 19.1.0 |
| `react-dom` | 19.1.0 |
| `react-native` | 0.81.5 |
| `react-native-gesture-handler` | ~2.28.0 |
| `react-native-paper` | ^5.15.0 |
| `react-native-reanimated` | ~4.1.1 |
| `react-native-safe-area-context` | ~5.6.0 |
| `react-native-screens` | ~4.16.0 |
| `react-native-web` | ~0.21.0 |
| `react-native-worklets` | 0.5.1 |
| `react-navigation` | ^5.0.0 |
| `zustand` | ^5.0.11 |

## 项目结构

```
poetry-app/
├── .vercel/
│   ├── project.json
├── .vscode/
│   ├── extensions.json
│   ├── settings.json
├── android/
│   ├── .gradle/
│   │   ├── 8.14.3/
│   │   ├── buildOutputCleanup/
│   │   ├── noVersion/
│   │   ├── vcs-1/
│   ├── .kotlin/
│   │   ├── sessions/
│   ├── app/
│   │   ├── .cxx/
│   │   ├── build/
│   │   ├── src/
│   ├── build/
│   │   ├── generated/
│   │   ├── reports/
│   ├── gradle/
│   │   ├── wrapper/
├── app/
│   ├── (tabs)/
│   │   ├── _layout.tsx
│   │   ├── favorites.tsx
│   │   ├── index.tsx
│   │   ├── profile.tsx
│   │   ├── search.tsx
│   ├── auth/
│   │   ├── login.tsx
│   │   ├── register.tsx
│   ├── poem/
│   │   ├── [id].tsx
│   ├── vip/
│   │   ├── index.tsx
│   ├── _layout.tsx
│   ├── modal.tsx
├── assets/
│   ├── images/
├── components/
│   ├── ui/
│   │   ├── collapsible.tsx
│   │   ├── icon-symbol.ios.tsx
│   │   ├── icon-symbol.tsx
│   ├── external-link.tsx
│   ├── haptic-tab.tsx
│   ├── hello-wave.tsx
│   ├── parallax-scroll-view.tsx
│   ├── themed-text.tsx
│   ├── themed-view.tsx
├── constants/
│   ├── theme.ts
├── data/
│   ├── processed/
│   │   ├── dynasties.json
│   │   ├── poems.json
│   │   ├── poets.json
│   ├── raw/
```

## 最近更新

| Commit | 说明 |
|--------|------|
| `4f9cd30` | feat: 保存改动 |
| `f2796f0` | feat:  保存本地翻译任务 |
| `a32991f` | feat:添加任务 |
| `351f20a` | 添加 |
| `e0c51a7` | iter-1: MVP功能完善 - 登录增强、VIP订阅、推送通知 |

---
*最后同步: 2026-04-18 12:00*
