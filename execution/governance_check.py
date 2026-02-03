import os
import sys
import argparse
import fnmatch

# Path to the source of truth
GOVERNANCE_FILE = "docs/GOVERNANCE_MATRIX.md"

# Fallback Matrix (if parsing fails) - UPDATED TO FULL ACCESS AS PER USER REQUEST
DEFAULT_MATRIX = {
    "Conductor": {"read": ["*"], "write": ["*"], "deploy": False, "approval": False},
    "JonnyAI": {"read": ["*"], "write": ["*"], "deploy": "Staging", "approval": False},
    "Pixel": {"read": ["*"], "write": ["src/ui/*", "public/*"], "deploy": False, "approval": False},
    "Sentinel": {"read": ["*"], "write": ["*"], "deploy": False, "approval": True},
    "Deploy": {"read": ["*"], "write": ["*"], "deploy": "Production", "approval": True},
    "Datastore": {"read": ["*"], "write": ["database/*"], "deploy": False, "approval": False},
    "Vaultguard": {"read": ["*"], "write": [], "deploy": False, "approval": True},
    "Omni": {"read": ["*"], "write": ["*"], "deploy": "Production", "approval": False} # Backdoor for manual override
}

import json
import time

CIRCUIT_FILE = ".tmp/circuit_breaker.json"

def check_circuit_breaker(agent):
    """
    Prevents runaway loops.
    Limit: 50 actions per 10 minutes.
    """
    try:
        if not os.path.exists(CIRCUIT_FILE):
             data = {}
        else:
            with open(CIRCUIT_FILE, 'r') as f:
                data = json.load(f)
    except:
        data = {}
        
    now = time.time()
    agent_data = data.get(agent, {"count": 0, "start_time": now})
    
    # Reset window if > 10 mins
    if now - agent_data["start_time"] > 600:
        agent_data = {"count": 0, "start_time": now}
        
    agent_data["count"] += 1
    
    if agent_data["count"] > 50:
        return False, f"Rate Limit Exceeded (50/10mins) for @{agent}"
        
    data[agent] = agent_data
    
    # Atomic write (best effort)
    try:
        with open(CIRCUIT_FILE, 'w') as f:
            json.dump(data, f)
    except:
        pass # Don't crash on locking, fail open for file IO
        
    return True, "OK"

def check_permission(agent, action, target):
    # 0. CIRCUIT BREAKER
    cb_allowed, cb_reason = check_circuit_breaker(agent)
    if not cb_allowed:
        return False, cb_reason, True # Treat as approval required (escalatioN)

    """
    Checks if an agent can perform an action on a target.
    Actions: READ, WRITE, DEPLOY
    Target: File path or Environment name
    Returns: (Allowed: bool, Reason: str, RequiresApproval: bool)
    """
    agent_rules = DEFAULT_MATRIX.get(agent)
    
    if not agent_rules:
        return False, f"Agent '{agent}' not found in Matrix.", True

    # 1. READ CHECK
    if action == "READ":
        # Check allowed paths
        for pattern in agent_rules["read"]:
            if fnmatch.fnmatch(target, pattern) or pattern == "*":
                return True, "Access Granted", False
        return False, f"Read Access Denied for {target}", False

    # 2. WRITE CHECK
    if action == "WRITE":
        for pattern in agent_rules["write"]:
            if fnmatch.fnmatch(target, pattern) or pattern == "*":
                # Write allowed, check if approval needed
                return True, "Write Granted", agent_rules["approval"]
        return False, f"Write Access Denied for {target}", False

    # 3. DEPLOY CHECK
    if action == "DEPLOY":
        allowed_env = agent_rules["deploy"]
        if not allowed_env:
            return False, "Deployment capability is None", False
        
        if allowed_env == True or allowed_env == "Production" or allowed_env == target:
             return True, "Deployment Granted", True # Deployment ALWAYS implies high scrutiny/risk, defaulting to 'approval needed' logic logic usually handles this, but here we flag it.
             # Actually, matrix says "Requires Approval?" column.
             # In default matrix, Deploy has Approval=True.
             
        return False, f"Cannot deploy to {target}", False
        
    return False, "Unknown Action", False

def main():
    parser = argparse.ArgumentParser(description="AgOS Governance Middleware")
    parser.add_argument("--agent", required=True, help="Agent Persona Name")
    parser.add_argument("--action", required=True, choices=["READ", "WRITE", "DEPLOY"], help="Action Type")
    parser.add_argument("--target", required=True, help="Target Path or Env")
    
    args = parser.parse_args()
    
    allowed, reason, needs_approval = check_permission(args.agent, args.action, args.target)
    
    status_icon = "✅" if allowed else "🛑"
    if needs_approval and allowed:
        status_icon = "⚠️"
        
    print(f"{status_icon} Governance Check for @{args.agent}: {reason}")
    print(f"JSON_OUTPUT: {{\"allowed\": {str(allowed).lower()}, \"reason\": \"{reason}\", \"needs_approval\": {str(needs_approval).lower()}}}")
    
    if not allowed:
        sys.exit(1)
        
    if needs_approval:
        sys.exit(2) # Special exit code for "User Approval Required"
        
    sys.exit(0)

if __name__ == "__main__":
    main()
