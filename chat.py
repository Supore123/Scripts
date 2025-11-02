#!/usr/bin/env python3
# DESC: Intelligent chat assistant with reasoning and natural language understanding
#       Uses semantic matching, context awareness, and conversational AI patterns

import subprocess
import json
import re
from pathlib import Path
from colorama import init, Fore, Style
from datetime import datetime
from collections import defaultdict

# ---------------------------
# Configuration
# ---------------------------
init(autoreset=True)
SCRIPTS_DIR = Path.home() / "Scripts"
BIN_DIR = Path("/usr/local/bin")
HISTORY_FILE = Path.home() / ".jychat_history"
CONTEXT_FILE = Path.home() / ".jychat_context.json"
JY_PREFIX = "jy"
MAX_HISTORY = 100

# ---------------------------
# Knowledge Base & Context
# ---------------------------
class KnowledgeBase:
    """Semantic understanding of commands and user intent"""

    SEMANTIC_GROUPS = {
        "media": ["play", "music", "audio", "video", "sound", "movie", "stream"],
        "file_ops": ["copy", "move", "delete", "backup", "sync", "file", "folder", "directory"],
        "network": ["download", "upload", "fetch", "url", "web", "internet", "api", "curl"],
        "system": ["process", "kill", "monitor", "status", "system", "cpu", "memory", "disk"],
        "notification": ["notify", "alert", "remind", "message", "send", "tell"],
        "search": ["find", "search", "locate", "grep", "look"],
        "text": ["edit", "write", "read", "text", "note", "document"],
        "dev": ["code", "compile", "build", "test", "deploy", "git", "commit"],
        "time": ["schedule", "timer", "alarm", "cron", "wait", "delay"],
    }

    ACTION_VERBS = {
        "start": ["start", "begin", "launch", "open", "run", "execute", "play", "turn on"],
        "stop": ["stop", "end", "terminate", "kill", "close", "turn off", "quit"],
        "show": ["show", "display", "list", "print", "get", "view", "see"],
        "modify": ["change", "update", "modify", "edit", "set", "configure"],
        "create": ["create", "make", "new", "add", "generate"],
        "delete": ["delete", "remove", "clear", "clean", "purge"],
    }

    @staticmethod
    def categorize_command(cmd_info):
        """Categorize command based on description and tags"""
        text = (cmd_info["desc"] + " " + " ".join(cmd_info.get("tags", []))).lower()
        categories = []
        for category, keywords in KnowledgeBase.SEMANTIC_GROUPS.items():
            if any(kw in text for kw in keywords):
                categories.append(category)
        return categories or ["general"]

    @staticmethod
    def extract_action(user_input):
        """Extract primary action from user input"""
        text = user_input.lower()
        for action, verbs in KnowledgeBase.ACTION_VERBS.items():
            if any(verb in text for verb in verbs):
                return action
        return "query"

class ConversationContext:
    """Maintains conversation state and memory"""

    def __init__(self):
        self.data = self.load()
        self.session_history = []
        self.last_command = None
        self.last_topic = None
        self.user_patterns = defaultdict(int)

    def load(self):
        if CONTEXT_FILE.exists():
            with open(CONTEXT_FILE, "r") as f:
                return json.load(f)
        return {
            "command_frequency": {},
            "successful_patterns": [],
            "failed_patterns": [],
            "preferences": {},
            "command_history": [],
            "conversation_topics": []
        }

    def save(self):
        with open(CONTEXT_FILE, "w") as f:
            json.dump(self.data, f, indent=2)

    def record_command(self, cmd, args, success):
        """Record command execution for learning"""
        entry = {
            "command": cmd,
            "args": args,
            "success": success,
            "timestamp": datetime.now().isoformat(),
            "context": self.last_topic
        }
        self.data["command_history"].append(entry)
        self.data["command_history"] = self.data["command_history"][-50:]

        if success:
            pattern = f"{self.last_topic}:{cmd}" if self.last_topic else cmd
            self.data["successful_patterns"].append(pattern)

        self.data["command_frequency"][cmd] = self.data["command_frequency"].get(cmd, 0) + 1
        self.last_command = cmd
        self.save()

    def get_likely_command(self, topic):
        """Predict likely command based on topic and history"""
        patterns = [p for p in self.data["successful_patterns"] if topic in p]
        if patterns:
            cmds = [p.split(":")[-1] for p in patterns]
            return max(set(cmds), key=cmds.count)
        return None

    def add_to_session(self, user_msg, bot_msg):
        """Add to session memory"""
        self.session_history.append({"user": user_msg, "bot": bot_msg, "time": datetime.now()})
        self.session_history = self.session_history[-20:]  # Keep last 20

# ---------------------------
# Load scripts with semantic analysis
# ---------------------------
script_context = {}
for file in SCRIPTS_DIR.glob("*.[ps][hy]*"):
    with open(file, "r") as f:
        lines = f.read().splitlines()
        desc = next((line.replace("# DESC:", "").strip() for line in lines if line.startswith("# DESC:")), "")
        args = [line.replace("# ARG:", "").strip() for line in lines if line.startswith("# ARG:")]
        tags = [line.replace("# TAG:", "").strip() for line in lines if line.startswith("# TAG:")]
        examples = [line.replace("# EXAMPLE:", "").strip() for line in lines if line.startswith("# EXAMPLE:")]

        info = {
            "type": "py" if file.suffix == ".py" else "sh",
            "desc": desc or "No description available",
            "args": args,
            "tags": tags,
            "examples": examples,
            "path": BIN_DIR / (JY_PREFIX + file.stem),
            "name": file.stem
        }
        info["categories"] = KnowledgeBase.categorize_command(info)
        script_context[file.stem] = info

context = ConversationContext()

# ---------------------------
# NLU Engine
# ---------------------------
class NLUEngine:
    """Natural Language Understanding with reasoning"""

    @staticmethod
    def parse(user_input, conversation_ctx):
        """Deep parsing with context awareness"""
        text = user_input.lower().strip()
        words = text.split()

        # Extract entities
        entities = {
            "action": KnowledgeBase.extract_action(text),
            "commands": [],
            "parameters": [],
            "temporal": NLUEngine.extract_temporal(text),
            "category": None,
            "intensity": NLUEngine.extract_intensity(text)
        }

        # Detect command references
        for cmd_name, cmd_info in script_context.items():
            # Direct match
            if cmd_name in text:
                entities["commands"].append(cmd_name)
                continue

            # Tag match
            for tag in cmd_info.get("tags", []):
                if tag.lower() in text:
                    entities["commands"].append(cmd_name)
                    break

            # Semantic match
            desc_words = set(cmd_info["desc"].lower().split())
            input_words = set(words)
            if len(desc_words & input_words) >= 2:
                entities["commands"].append(cmd_name)

        # Detect category if no direct command
        if not entities["commands"]:
            for category, keywords in KnowledgeBase.SEMANTIC_GROUPS.items():
                if any(kw in text for kw in keywords):
                    entities["category"] = category
                    break

        # Extract potential parameters (quoted strings, paths, numbers)
        entities["parameters"].extend(re.findall(r'"([^"]*)"', user_input))
        entities["parameters"].extend(re.findall(r"'([^']*)'", user_input))
        entities["parameters"].extend(re.findall(r'/[^\s]+', user_input))
        entities["parameters"].extend(re.findall(r'\d+', user_input))

        return entities

    @staticmethod
    def extract_temporal(text):
        """Extract time-related information"""
        if any(w in text for w in ["now", "immediately", "asap"]):
            return "immediate"
        if any(w in text for w in ["later", "schedule", "wait"]):
            return "delayed"
        if any(w in text for w in ["again", "repeat", "keep"]):
            return "recurring"
        return None

    @staticmethod
    def extract_intensity(text):
        """Detect urgency or importance"""
        urgent = ["urgent", "asap", "now", "quick", "fast", "immediately"]
        if any(w in text for w in urgent):
            return "high"
        return "normal"

class ReasoningEngine:
    """Multi-step reasoning and decision making"""

    @staticmethod
    def find_best_match(entities, conversation_ctx):
        """Find best command match using multiple signals"""
        candidates = []

        # Direct command matches
        for cmd in entities["commands"]:
            if cmd in script_context:
                candidates.append((cmd, 1.0, "direct"))

        # Category-based matches
        if entities["category"] and not candidates:
            for cmd_name, cmd_info in script_context.items():
                if entities["category"] in cmd_info["categories"]:
                    # Score based on command frequency and relevance
                    freq = conversation_ctx.data["command_frequency"].get(cmd_name, 0)
                    score = 0.6 + (min(freq, 10) * 0.04)  # Up to 1.0
                    candidates.append((cmd_name, score, "category"))

        # Context-based prediction
        if conversation_ctx.last_topic and not candidates:
            predicted = conversation_ctx.get_likely_command(conversation_ctx.last_topic)
            if predicted:
                candidates.append((predicted, 0.5, "context"))

        # Semantic fuzzy matching
        if not candidates:
            candidates.extend(ReasoningEngine.semantic_search(entities))

        # Sort by score
        if candidates:
            candidates.sort(key=lambda x: x[1], reverse=True)
            return candidates[0][0], candidates[0][2]

        return None, None

    @staticmethod
    def semantic_search(entities):
        """Deep semantic search through commands"""
        candidates = []
        action = entities["action"]

        for cmd_name, cmd_info in script_context.items():
            score = 0.0
            desc = cmd_info["desc"].lower()

            # Action alignment
            if action == "start" and any(w in desc for w in ["run", "start", "launch", "play"]):
                score += 0.3
            elif action == "stop" and any(w in desc for w in ["stop", "kill", "end"]):
                score += 0.3
            elif action == "show" and any(w in desc for w in ["show", "list", "display", "get"]):
                score += 0.3

            # Parameter compatibility
            if entities["parameters"] and cmd_info["args"]:
                score += 0.2

            if score > 0.2:
                candidates.append((cmd_name, score, "semantic"))

        return candidates

    @staticmethod
    def plan_execution(entities, conversation_ctx):
        """Create execution plan"""
        plan = {
            "steps": [],
            "requires_confirmation": False,
            "estimated_risk": "low"
        }

        # Find primary command
        cmd, method = ReasoningEngine.find_best_match(entities, conversation_ctx)

        if not cmd:
            return None

        # Build step
        step = {
            "command": cmd,
            "args": entities["parameters"],
            "background": ReasoningEngine.should_run_background(cmd),
            "method": method
        }

        plan["steps"].append(step)

        # Risk assessment
        dangerous_actions = ["delete", "remove", "kill", "stop", "format"]
        if any(d in script_context[cmd]["desc"].lower() for d in dangerous_actions):
            plan["estimated_risk"] = "medium"
            plan["requires_confirmation"] = True

        return plan

    @staticmethod
    def should_run_background(cmd):
        """Determine if command should run in background"""
        if not cmd:
            return False
        desc = script_context.get(cmd, {}).get("desc", "").lower()
        bg_keywords = ["music", "server", "monitor", "watch", "daemon", "service"]
        return any(kw in desc for kw in bg_keywords)

# ---------------------------
# Response Generator
# ---------------------------
class ResponseGenerator:
    """Generate intelligent, contextual responses"""

    @staticmethod
    def generate(user_input, conversation_ctx):
        """Main response generation"""
        text = user_input.lower()

        # Meta-commands
        if text in ["exit", "quit", "bye", "goodbye"]:
            return None, "exit"

        # Help requests
        if text == "help" or text == "?":
            return ResponseGenerator.generate_help(), "help"

        if text.startswith("help "):
            cmd = text.replace("help ", "").strip()
            if cmd in script_context:
                return ResponseGenerator.format_detailed_help(cmd), "help"

        # Analytics queries
        if "most" in text and ("used" in text or "popular" in text):
            return ResponseGenerator.show_analytics(conversation_ctx), "analytics"

        if "what can" in text or "what do you" in text or "capabilities" in text:
            return ResponseGenerator.explain_capabilities(), "info"

        if "history" in text or "recent" in text:
            return ResponseGenerator.show_history(conversation_ctx), "history"

        # Parse and reason
        entities = NLUEngine.parse(user_input, conversation_ctx)
        plan = ReasoningEngine.plan_execution(entities, conversation_ctx)

        if not plan:
            return ResponseGenerator.no_match_response(entities, conversation_ctx), "no_match"

        # Execute plan
        if plan["requires_confirmation"]:
            cmd = plan["steps"][0]["command"]
            return f"⚠️  '{cmd}' may modify system state. Type 'yes' to continue or rephrase.", "confirm"

        return ResponseGenerator.execute_plan(plan, conversation_ctx), "execute"

    @staticmethod
    def execute_plan(plan, conversation_ctx):
        """Execute the planned steps"""
        results = []

        for step in plan["steps"]:
            cmd = step["command"]
            args = step["args"]

            # Execute
            success, output = execute_command(cmd, args, step["background"])
            conversation_ctx.record_command(cmd, args, success)

            # Format output
            if step["method"] == "direct":
                result = output
            else:
                confidence = "✓" if step["method"] == "direct" else "~"
                result = f"{confidence} [{cmd}] {output}"

            results.append(result)

        return "\n".join(results)

    @staticmethod
    def no_match_response(entities, conversation_ctx):
        """Intelligent fallback when no match found"""
        # Try to suggest based on category
        if entities["category"]:
            cmds = [name for name, info in script_context.items()
                   if entities["category"] in info["categories"]]
            if cmds:
                suggestions = ", ".join(cmds[:3])
                return f"💡 I found some {entities['category']}-related commands: {suggestions}\n   Try: 'help {cmds[0]}' or 'run {cmds[0]}'"

        # Suggest based on action
        action = entities["action"]
        action_cmds = []
        for name, info in script_context.items():
            desc = info["desc"].lower()
            if action in desc or any(w in desc for w in KnowledgeBase.ACTION_VERBS.get(action, [])):
                action_cmds.append(name)

        if action_cmds:
            return f"🤔 For '{action}' actions, try: {', '.join(action_cmds[:3])}"

        return "❓ I'm not sure what you want. Try:\n  • 'help' - see all commands\n  • 'what can you do?' - learn capabilities\n  • Describe what you want to accomplish"

    @staticmethod
    def generate_help():
        """Smart help organized by category"""
        categories = defaultdict(list)
        for name, info in script_context.items():
            for cat in info["categories"]:
                categories[cat].append(name)

        output = [f"{Fore.CYAN}📚 Available Commands by Category:{Style.RESET_ALL}\n"]

        for category, cmds in sorted(categories.items()):
            output.append(f"{Fore.YELLOW}{category.upper()}{Style.RESET_ALL}")
            for cmd in sorted(cmds):
                info = script_context[cmd]
                output.append(f"  • {cmd} - {info['desc'][:60]}")

        output.append(f"\n💬 Natural language examples:")
        output.append("  • 'play some music'")
        output.append("  • 'backup my files to /backup'")
        output.append("  • 'what are my most used commands?'")

        return "\n".join(output)

    @staticmethod
    def format_detailed_help(cmd):
        """Detailed command help"""
        info = script_context[cmd]
        output = [f"\n{Fore.CYAN}━━━ {cmd} ━━━{Style.RESET_ALL}"]
        output.append(f"📝 {info['desc']}")

        if info["args"]:
            output.append(f"\n{Fore.YELLOW}Arguments:{Style.RESET_ALL}")
            for arg in info["args"]:
                output.append(f"  • {arg}")

        if info["tags"]:
            output.append(f"\n{Fore.YELLOW}Tags:{Style.RESET_ALL} {', '.join(info['tags'])}")

        if info["examples"]:
            output.append(f"\n{Fore.YELLOW}Examples:{Style.RESET_ALL}")
            for ex in info["examples"]:
                output.append(f"  $ {ex}")

        return "\n".join(output)

    @staticmethod
    def show_analytics(conversation_ctx):
        """Show usage analytics"""
        freq = conversation_ctx.data["command_frequency"]
        if not freq:
            return "📊 No commands used yet."

        total = sum(freq.values())
        top = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:5]

        output = [f"📊 Command Analytics (Total: {total}):\n"]
        for cmd, count in top:
            pct = (count / total) * 100
            bar = "█" * int(pct / 5)
            output.append(f"  {cmd:15} {bar} {count} ({pct:.1f}%)")

        return "\n".join(output)

    @staticmethod
    def show_history(conversation_ctx):
        """Show recent command history"""
        history = conversation_ctx.data["command_history"][-10:]
        if not history:
            return "📜 No command history."

        output = ["📜 Recent Commands:\n"]
        for entry in reversed(history):
            time = datetime.fromisoformat(entry["timestamp"]).strftime("%H:%M")
            status = "✓" if entry["success"] else "✗"
            args_str = " ".join(entry["args"]) if entry["args"] else ""
            output.append(f"  {time} {status} {entry['command']} {args_str}")

        return "\n".join(output)

    @staticmethod
    def explain_capabilities():
        """Explain what the bot can do"""
        return f"""{Fore.CYAN}🤖 I'm an intelligent command assistant. I can:{Style.RESET_ALL}

✅ Understand natural language
   • "play music" → finds and runs music command
   • "backup my files" → executes backup with context

✅ Learn from your usage
   • Tracks frequency and patterns
   • Predicts what you likely want

✅ Smart matching
   • Fuzzy matching, tags, categories
   • Semantic understanding of descriptions

✅ Provide analytics
   • "most used commands" → usage stats
   • "history" → recent executions

✅ Execute safely
   • Risk assessment
   • Background processes for long-running tasks

Try asking me to do something or type 'help' to see all commands!"""

# ---------------------------
# Command Execution
# ---------------------------
def execute_command(cmd_name, args, background=False):
    """Execute command and return success status and output"""
    cmd_info = script_context.get(cmd_name)
    if not cmd_info or not cmd_info["path"].exists():
        return False, f"Command '{JY_PREFIX}{cmd_name}' not found"

    cmd_args = [str(cmd_info["path"])] + (args or [])

    try:
        if background:
            subprocess.Popen(cmd_args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True, f"Started in background"
        else:
            result = subprocess.run(cmd_args, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                output = result.stdout.strip() or "Success"
                return True, output
            else:
                error = result.stderr.strip() or "Command failed"
                return False, error
    except subprocess.TimeoutExpired:
        return False, "Timeout (30s)"
    except Exception as e:
        return False, f"Error: {e}"

# ---------------------------
# Main Loop
# ---------------------------
def main():
    print(f"{Fore.CYAN}╔═══════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║   🤖 Intelligent jy Assistant        ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║   {len(script_context)} commands loaded · AI-powered    ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚═══════════════════════════════════════╝{Style.RESET_ALL}")
    print(f"\n💡 Try: 'what can you do?' or just describe what you need!\n")

    while True:
        try:
            user_input = input(f"{Fore.GREEN}You: {Style.RESET_ALL}").strip()
            if not user_input:
                continue

            # Generate response
            response, response_type = ResponseGenerator.generate(user_input, context)

            if response_type == "exit":
                print(f"{Fore.CYAN}👋 Goodbye! Executed {sum(context.data['command_frequency'].values())} commands this session.{Style.RESET_ALL}")
                break

            # Update topic tracking
            entities = NLUEngine.parse(user_input, context)
            if entities["category"]:
                context.last_topic = entities["category"]

            print(f"{Fore.MAGENTA}Bot: {Style.RESET_ALL}{response}\n")
            context.add_to_session(user_input, response)

        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}⚠️  Interrupted. Type 'exit' to quit.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
