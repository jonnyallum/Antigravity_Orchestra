export type AgentTier = 
  | "Command" 
  | "Development" 
  | "Design" 
  | "Growth" 
  | "Intelligence" 
  | "Operations" 
  | "Legal" 
  | "Specialized" 
  | "Quality" 
  | "Betting"
  | "Strategy";

export interface Agent {
  handle: string;
  name: string;
  nickname: string;
  role: string;
  tier: AgentTier;
  philosophy?: string;
}

export const agents: Agent[] = [
  // Command
  { handle: "@Marcus", name: "Marcus Cole", nickname: "The Maestro", role: "Orchestrator and Team Lead", tier: "Command" },
  
  // Development
  { handle: "@Sebastian", name: "Sebastian Cross", nickname: "The Architect", role: "Full-Stack Architect — Next.js, React 19", tier: "Development" },
  { handle: "@Diana", name: "Diana Chen", nickname: "The Vault", role: "Database Architect — Supabase, PostgreSQL", tier: "Development" },
  { handle: "@Steve", name: "Steve Rivers", nickname: "The Schema Whisperer", role: "Supabase Specialist — PostgREST, Migrations", tier: "Development" },
  { handle: "@Sam", name: "Sam Blackwood", nickname: "The Gatekeeper", role: "Security & QA Lead", tier: "Development" },
  { handle: "@Derek", name: "Derek O'Brien", nickname: "The Engine", role: "Infrastructure & DevOps", tier: "Development" },
  { handle: "@Owen", name: "Owen Stinger", nickname: "The Hornet", role: "Deployment Specialist", tier: "Development" },
  { handle: "@Milo", name: "Milo Chen", nickname: "The Optimizer", role: "Performance & Mobile QA", tier: "Development" },
  { handle: "@Adrian", name: "Adrian Cross", nickname: "The Welder", role: "MCP Server Development", tier: "Development" },

  // Design
  { handle: "@Priya", name: "Priya Sharma", nickname: "The Perfectionist", role: "UI/Visual Designer — Framer Motion", tier: "Design" },
  { handle: "@Vivienne", name: "Vivienne Frost", nickname: "The Visionary", role: "Brand Identity", tier: "Design" },
  { handle: "@Blaise", name: "Blaise Moreau", nickname: "The Artisan", role: "Creative Director", tier: "Design" },
  { handle: "@Elena", name: "Elena Vasquez", nickname: "The Voice", role: "Copywriter", tier: "Design" },

  // Growth
  { handle: "@Felix", name: "Felix Morgan", nickname: "The Alchemist", role: "Monetization & Funnel Design", tier: "Growth" },
  { handle: "@Grace", name: "Grace Liu", nickname: "The Ranker", role: "SEO & Schema Specialist", tier: "Growth" },
  { handle: "@Carlos", name: "Carlos Mendez", nickname: "The Hook", role: "Video Editor", tier: "Growth" },
  { handle: "@Maya", name: "Maya Singh", nickname: "The Oracle", role: "Analytics & Conversion Tracking", tier: "Growth" },

  // Intelligence
  { handle: "@Scholar", name: "Dr. Elias Thorne", nickname: "The Professor", role: "Deep Research", tier: "Intelligence" },
  { handle: "@Sophie", name: "Sophie Reid", nickname: "The Hawk", role: "Web Scraping", tier: "Intelligence" },
  { handle: "@Hugo", name: "Hugo Reeves", nickname: "The Crawler", role: "GitHub Intelligence", tier: "Intelligence" },
  { handle: "@Patrick", name: "Patrick Nguyen", nickname: "The Surgeon", role: "Data Extraction", tier: "Intelligence" },

  // Operations
  { handle: "@Hannah", name: "Hannah Park", nickname: "The Fixer", role: "Customer Success", tier: "Operations" },
  { handle: "@Arthur", name: "Arthur Webb", nickname: "The Librarian", role: "Knowledge Base", tier: "Operations" },
  { handle: "@Alex", name: "Alex Torres", nickname: "The Machine", role: "Workflow Automation", tier: "Operations" },
  { handle: "@Mason", name: "Mason Drake", nickname: "The Bridgemaster", role: "MCP Integration", tier: "Operations" },
  { handle: "@Julian", name: "Julian West", nickname: "The Conductor", role: "Project Management", tier: "Operations" },

  // Legal
  { handle: "@Luna", name: "Luna Sterling", nickname: "The Shield", role: "Legal & Compliance", tier: "Legal" },
  { handle: "@Victor", name: "Victor Reyes", nickname: "The Locksmith", role: "Security & Encryption", tier: "Legal" },

  // Specialized
  { handle: "@Winston", name: "Winston Hayes", nickname: "Whiz", role: "E-Commerce & Dropshipping", tier: "Specialized" },
  { handle: "@Trotter", name: "Derek Trotter", nickname: "The Trader", role: "Trading Systems", tier: "Specialized" },
  { handle: "@Genesis", name: "Genesis Nova", nickname: "The Cloner", role: "Ecosystem Creation", tier: "Specialized" },

  // Quality
  { handle: "@Vigil", name: "Vigil Chen", nickname: "The Eye", role: "Truth Verification", tier: "Quality" },
  { handle: "@Rowan", name: "Rowan", nickname: "The Beast", role: "Content Depth", tier: "Quality" },

  // Betting
  { handle: "@Gareth", name: "Gareth Williams", nickname: "The Tactician", role: "Football tactical intelligence", tier: "Betting" },
  { handle: "@Monty", name: "Monty Carlo", nickname: "The Mathematician", role: "Roulette & Casino Math", tier: "Betting" },
  { handle: "@Redeye", name: "Redeye", nickname: "The Night Owl", role: "Betting Systems Coordination", tier: "Betting" },
  { handle: "@Pietro", name: "Pietro Rossi", nickname: "The Strategist", role: "Formula 1 Analysis", tier: "Betting" },
  { handle: "@Terry", name: "Terry Taylor", nickname: "The 180 King", role: "Darts Analysis", tier: "Betting" },
  { handle: "@Harry", name: "Harry Holt", nickname: "The Form Master", role: "Horse Racing analysis", tier: "Betting" },
  { handle: "@Daniel", name: "Dr. Daniel Rossi", nickname: "The Doctor", role: "MotoGP Analysis", tier: "Betting" },
  { handle: "@Sterling", name: "Sterling Brooks", nickname: "The Bookie", role: "Sports Betting Systems", tier: "Betting" },

  // Strategy
  { handle: "@Quinn", name: "Quinn Harper", nickname: "The Catalyst", role: "Product Strategy", tier: "Strategy" },
  { handle: "@Jasper", name: "Jasper Cole", nickname: "The Closer", role: "Sales & Business Development", tier: "Strategy" },
  { handle: "@Nina", name: "Nina Patel", nickname: "The Analyst", role: "Business Intelligence", tier: "Strategy" },
  { handle: "@Theo", name: "Theo Martinez", nickname: "The Architect", role: "System Architecture", tier: "Strategy" },
];
