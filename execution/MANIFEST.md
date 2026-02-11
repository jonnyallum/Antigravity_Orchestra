# Execution Scripts Manifest
> Last Updated: 2026-02-11 | 76 active scripts | 39 archived

## Core Infrastructure
| Script | Purpose | Owner |
|:-------|:--------|:------|
| `validate_agents.py` | SKILL.md compliance checking | @Marcus |
| `feedback_engine.py` | Task logging, health metrics, gap detection | @Marcus |
| `memory_quality_gate.py` | Learning validation before storage | @Vigil |
| `orchestra_heartbeat.py` | Detect idle/ghosted agents | @Marcus |
| `auto_commit.py` | Smart commit message generation | @Alex |
| `context_loader.py` | Session context loading | @Marcus |
| `conductor_toolkit.py` | Orchestration utilities | @Marcus |
| `workspace_analyzer.py` | Workspace health analysis | @Marcus |
| `health_dashboard.py` | Agent health dashboard | @Marcus |
| `session_logger.py` | Session activity logging | @Marcus |
| `inter_ai_validator.py` | Cross-AI communication validation | @Marcus |
| `ping_agent.py` | Agent availability check | @Marcus |
| `agent_summoner.py` | Summon specific agent personas | @Marcus |

## Deployment
| Script | Purpose | Owner |
|:-------|:--------|:------|
| `deploy_jonnyai.py` | JonnyAI website deployment | @Owen |
| `deploy_kwizz.py` | Kwizz app deployment | @Owen |
| `deploy_djwaste.py` | DJ Waste deployment | @Owen |
| `deploy_ftp.py` | Generic FTP deployment | @Owen |
| `deploy_ssh.py` | Generic SSH deployment | @Owen |
| `deploy_v4.py` | Insydetradar deployment | @Owen |
| `verify_deploy.py` | Post-deploy verification | @Owen |
| `test_hostinger_ssh.py` | SSH connectivity test | @Derek |

## Client: Kwizz
| Script | Purpose | Owner |
|:-------|:--------|:------|
| `apply_kwizz_base_schema.py` | Base DB schema | @Diana |
| `apply_kwizz_monetization_schema.py` | Monetization schema | @Diana |
| `check_kwizz_supabase.py` | Supabase health check | @Steve |
| `configure_kwizz_supabase.py` | Supabase configuration | @Steve |
| `diagnose_kwizz.py` | Kwizz diagnostics | @Sebastian |
| `enable_kwizz_realtime.py` | Realtime subscriptions | @Steve |
| `generate_kwizz_packs.py` | Quiz pack generation | @Sebastian |
| `bulk_import_trivia.py` | Trivia data import | @Sebastian |
| `check_quiz_count.py` | Quiz count verification | @Sebastian |
| `test_kwizz_game_flow.py` | Game flow testing | @Sam |
| `verify_kwizz_monetization.py` | Monetization verification | @Felix |
| `mcp_supabase_kwizz.py` | MCP Supabase bridge | @Steve |

## Client: HACCP (Village Bakery)
| Script | Purpose | Owner |
|:-------|:--------|:------|
| `fetch_haccp_sheets.py` | Fetch HACCP templates | @Sebastian |
| `fill_haccp_temps.py` | Fill temperature sheets | @Sebastian |
| `fill_haccp_other_sheets.py` | Fill other HACCP sheets | @Sebastian |
| `consolidate_haccp.py` | Consolidate all HACCP data | @Sebastian |

## Client: Insydetradar
| Script | Purpose | Owner |
|:-------|:--------|:------|
| `check_supabase.py` | Supabase health check | @Steve |
| `setup_supabase_leads.py` | Leads table setup | @Diana |
| `test_leads_insert.py` | Leads insert testing | @Sam |
| `verify_api_integration.py` | API integration check | @Sam |
| `check_cors.py` | CORS configuration check | @Derek |
| `check_rpc_endpoint.py` | RPC endpoint check | @Steve |
| `test_broker_handshake.py` | Broker handshake test | @Sam |

## Brain / Supabase Intelligence
| Script | Purpose | Owner |
|:-------|:--------|:------|
| `brain_sync.py` | Brain database sync | @Diana |
| `brain_sync_protocol.py` | Brain sync protocol | @Diana |
| `brain_cli.py` | Brain CLI interface | @Diana |
| `expand_brain_final.py` | Brain expansion | @Diana |
| `expand_brain_for_website.py` | Website brain data | @Diana |
| `expand_tasks_for_cron.py` | Cron task expansion | @Alex |
| `get_brain_agents.py` | Get brain agent data | @Diana |
| `add_research_task.py` | Add research tasks | @Sophie |
| `populate_value_tasks.py` | Populate value tasks | @Felix |
| `verify_migration_002.py` | Migration verification | @Diana |
| `check_schedule.py` | Schedule checking | @Alex |
| `check_news.py` | News feed checking | @Sophie |

## System Maintenance
| Script | Purpose | Owner |
|:-------|:--------|:------|
| `purge_redundant.py` | Remove redundant files | @Marcus |
| `remove_nul_files.py` | Remove NUL files | @Marcus |
| `cleanup_legacy_bets.py` | Clean legacy betting data | @Marcus |
| `make_paste_file.py` | Create paste-ready files | @Marcus |
| `fix_agent_count.py` | Fix agent count references | @Marcus |
| `organize_agents.py` | Organize agent files | @Marcus |

## Upgrades & Audits
| Script | Purpose | Owner |
|:-------|:--------|:------|
| `upgrade_to_jaios4.py` | Jai.OS 4.0 upgrade | @Marcus |
| `upgrade_skills_opus.py` | Skills upgrade via Opus | @Marcus |
| `upgrade_project_readmes.py` | README upgrades | @Marcus |
| `audit_orchestra.py` | Orchestra audit | @Marcus |
| `audit_skills_opus.py` | Skills audit via Opus | @Marcus |
| `redteam_scan.py` | Security red team scan | @Sam |
| `create_audit_gallery.py` | Audit gallery creation | @Marcus |

## Ecosystem & Scaffolding
| Script | Purpose | Owner |
|:-------|:--------|:------|
| `init_workspace.py` | Initialize new workspace | @Marcus |
| `project_scaffolder.py` | Scaffold new projects | @Sebastian |
| `hotswap_ecosystem.py` | Swap ecosystem configs | @Marcus |
| `sync_ecosystem.py` | Sync ecosystem data | @Marcus |
| `sync_to_website.py` | Sync data to website | @Owen |
| `get_open_prs.py` | Get open pull requests | @Alex |

## Testing
| Script | Purpose | Owner |
|:-------|:--------|:------|
| `test_a0_api.py` | Agent Zero API test | @Sam |

---

## Archive (`execution/archive/`)
39 scripts archived on 2026-02-11. These are one-off logo generators, resolved fix scripts, and obsolete debug tools. They can be restored if needed.
