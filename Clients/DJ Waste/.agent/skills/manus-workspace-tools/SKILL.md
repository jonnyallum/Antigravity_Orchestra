---
name: manus-workspace-tools
description: Preservation of Manus-specific debug and runtime plugins.
---

# Manus Workspace Tools

This skill preserves the specific plugins used for debugging and runtime collection within the Manus environment.

## ⚠️ CRITICAL WARNING: Production Build Issue
These plugins, specifically `vitePluginManusDebugCollector`, inject a massive inlined runtime into `index.html`. 
**DO NOT use these in production deployments outside the Manus environment**, as they cause a "White Screen of Death" by misconfiguring MIME types and injecting incompatible scripts.

## Plugins

### 1. `vitePluginManusDebugCollector`
Collects browser console logs, network requests, and session replays, writing them to `.manus-logs/`.

```typescript
function vitePluginManusDebugCollector(): Plugin {
  return {
    name: "manus-debug-collector",

    transformIndexHtml(html) {
      if (process.env.NODE_ENV === "production") {
        return html;
      }
      return {
        html,
        tags: [
          {
            tag: "script",
            attrs: {
              src: "/__manus__/debug-collector.js",
              defer: true,
            },
            injectTo: "head",
          },
        ],
      };
    },

    configureServer(server: ViteDevServer) {
      server.middlewares.use("/__manus__/logs", (req, res, next) => {
        if (req.method !== "POST") {
          return next();
        }

        const handlePayload = (payload: any) => {
          if (payload.consoleLogs?.length > 0) {
            writeToLogFile("browserConsole", payload.consoleLogs);
          }
          if (payload.networkRequests?.length > 0) {
            writeToLogFile("networkRequests", payload.networkRequests);
          }
          if (payload.sessionEvents?.length > 0) {
            writeToLogFile("sessionReplay", payload.sessionEvents);
          }

          res.writeHead(200, { "Content-Type": "application/json" });
          res.end(JSON.stringify({ success: true }));
        };

        // ... body parsing logic ...
      });
    },
  };
}
```

### 2. `vitePluginManusRuntime`
External plugin from `vite-plugin-manus-runtime`. Used for environment-specific runtime features.

## Lessons Learned
- **MIME Type Conflict**: In production, the inlined scripts can cause the browser to interpret `.js` files as `text/html`, leading to module load failures.
- **Cleanup**: Always verify `vite.config.ts` during deployment to standard hosting (Hostinger/Vercel) to ensure internal debug tools are stripped.
