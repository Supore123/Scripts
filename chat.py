#!/usr/bin/env python3
# DESC: Ultra-intelligent chat assistant with deep script understanding
# TAG: chat, assistant, ai, helper

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
# Deep Script Parser
# ---------------------------
class ScriptParser:
    """Extract rich metadata from scripts"""

    @staticmethod
    def parse_script(file_path):
        """Deep parse script for all metadata"""
        with open(file_path, "r") as f:
            content = f.read()
            lines = content.splitlines()

        metadata = {
            "type": "py" if file_path.suffix == ".py" else "sh",
            "desc": "",
            "args": [],
            "tags": [],
            "examples": [],
            "usage": [],
            "flags": [],
            "subcommands": {},
            "requires": [],
            "path": BIN_DIR / (JY_PREFIX + file_path.stem),
            "name": file_path.stem
        }

        # Extract DESC
        for line in lines:
            if line.strip().startswith("# DESC:"):
                metadata["desc"] = line.replace("# DESC:", "").strip()
                break

        # Extract all metadata
        for line in lines:
            line = line.strip()
            if line.startswith("# ARG:"):
                metadata["args"].append(line.replace("# ARG:", "").strip())
            elif line.startswith("# TAG:"):
                metadata["tags"].extend([t.strip() for t in line.replace("# TAG:", "").split(",")])
            elif line.startswith("# EXAMPLE:"):
                metadata["examples"].append(line.replace("# EXAMPLE:", "").strip())

        # Parse argparse for Python scripts
        if metadata["type"] == "py":
            ScriptParser._parse_python_args(content, metadata)
        # Parse case statements for bash scripts
        elif metadata["type"] == "sh":
            ScriptParser._parse_bash_args(content, metadata)

        return metadata

    @staticmethod
    def _parse_python_args(content, metadata):
        """Extract argparse arguments from Python scripts"""
        # Find add_argument calls
        arg_pattern = r'add_argument\([\'"]([^"\']+)[\'"].*?help=[\'"]([^"\']+)[\'"]'
        for match in re.finditer(arg_pattern, content, re.DOTALL):
            flag = match.group(1)
            help_text = match.group(2)
            metadata["flags"].append(f"{flag} - {help_text}")

        # Also check for positional arguments
        positional_pattern = r'add_argument\([\'"]([a-z_]+)[\'"].*?help=[\'"]([^"\']+)[\'"]'
        for match in re.finditer(positional_pattern, content):
            arg = match.group(1)
            if not arg.startswith("-"):
                help_text = match.group(2)
                if f"{arg} - {help_text}" not in metadata["flags"]:
                    metadata["args"].append(f"{arg} - {help_text}")

    @staticmethod
    def _parse_bash_args(content, metadata):
        """Extract case statements and functions from bash scripts"""
        # Find case options
        case_pattern = r'case.*?in(.*?)esac'
        matches = re.findall(case_pattern, content, re.DOTALL)
        for match in matches:
            # Extract individual cases
            option_pattern = r'([a-z_-]+)\)'
            options = re.findall(option_pattern, match)
            for opt in options:
                if opt not in ["*", "help"]:
                    metadata["subcommands"][opt] = f"Subcommand: {opt}"

# ---------------------------
# Enhanced Knowledge Base
# ---------------------------
class KnowledgeBase:
    """Deep semantic understanding with script-specific knowledge"""

    SEMANTIC_GROUPS = {
        "media": ["play", "music", "audio", "video", "sound", "movie", "stream", "spotify", "airpods"],
        "file_ops": ["copy", "move", "delete", "backup", "sync", "file", "folder", "directory", "notes"],
        "network": ["download", "upload", "fetch", "url", "web", "internet", "api", "curl", "ssh", "connect"],
        "system": ["process", "kill", "monitor", "status", "system", "cpu", "memory", "disk", "info", "sysinfo"],
        "notification": ["notify", "alert", "remind", "message", "send", "tell"],
        "search": ["find", "search", "locate", "grep", "look"],
        "text": ["edit", "write", "read", "text", "note", "document"],
        "dev": ["code", "compile", "build", "test", "deploy", "git", "commit", "update"],
        "bluetooth": ["bluetooth", "airpods", "connect", "pair", "device", "audio"],
        "utils": ["utility", "helper", "tool", "utils", "clear", "echo", "date", "disk", "mem"]
    }

    # Command-specific synonyms learned from your scripts
    COMMAND_SYNONYMS = {
        "music": ["play music", "spotify", "play song", "tune", "track", "playlist", "skip", "pause", "next", "previous", "volume"],
        "airpods": ["connect airpods", "bluetooth", "headphones", "pair", "battery"],
        "sysinfo": ["system info", "system status", "stats", "computer info", "hardware", "specs"],
        "ssh": ["remote", "server", "connect to", "terminal"],
        "notes": ["commit notes", "push notes", "save notes", "sync notes", "backup notes"],
        "utils": ["utility", "echo", "clear screen", "disk space", "memory", "list files"],
        "update": ["update scripts", "refresh commands", "install scripts"]
    }

    ACTION_VERBS = {
        "start": ["start", "begin", "launch", "open", "run", "execute", "play", "turn on", "enable"],
        "stop": ["stop", "end", "terminate", "kill", "close", "turn off", "quit", "pause"],
        "show": ["show", "display", "list", "print", "get", "view", "see", "check", "status"],
        "modify": ["change", "update", "modify", "edit", "set", "configure", "adjust"],
        "create": ["create", "make", "new", "add", "generate", "write"],
        "delete": ["delete", "remove", "clear", "clean", "purge"],
        "connect": ["connect", "pair", "link", "join", "attach"],
        "disconnect": ["disconnect", "unpair", "unlink", "detach"],
        "sync": ["sync", "synchronize", "backup", "save", "commit", "push"]
    }

    @staticmethod
    def categorize_command(cmd_info):
        """Enhanced categorization with script-specific knowledge"""
        text = (cmd_info["desc"] + " " + " ".join(cmd_info.get("tags", []))).lower()
        categories = []

        for category, keywords in KnowledgeBase.SEMANTIC_GROUPS.items():
            if any(kw in text for kw in keywords):
                categories.append(category)

        # Add category based on command name
        name = cmd_info["name"].lower()
        if "music" in name:
            categories.append("media")
        if "ssh" in name:
            categories.append("network")
        if "note" in name:
            categories.append("file_ops")
        if "info" in name or "sys" in name:
            categories.append("system")
        if "airpod" in name or "bluetooth" in name:
            categories.append("bluetooth")

        return list(set(categories)) or ["general"]

    @staticmethod
    def extract_action(user_input):
        """Enhanced action extraction with music-specific commands"""
        text = user_input.lower()

        # Music-specific actions
        music_actions = {
            "skip": "next", "next": "next", "forward": "next",
            "back": "previous", "previous": "previous", "prev": "previous",
            "pause": "stop", "resume": "start", "unpause": "start",
            "shuffle": "shuffle", "random": "shuffle",
            "volume": "modify", "vol": "modify"
        }

        for trigger, action in music_actions.items():
            if trigger in text:
                return action

        # Standard actions
        for action, verbs in KnowledgeBase.ACTION_VERBS.items():
            if any(verb in text for verb in verbs):
                return action

        return "query"

    @staticmethod
    def find_synonyms(query, cmd_name):
        """Check if query matches command synonyms"""
        query = query.lower()
        if cmd_name in KnowledgeBase.COMMAND_SYNONYMS:
            synonyms = KnowledgeBase.COMMAND_SYNONYMS[cmd_name]
            for syn in synonyms:
                if syn in query:
                    return True
        return False

# ---------------------------
# Conversation Context with Learning
# ---------------------------
class ConversationContext:
    """Enhanced context with multi-turn awareness"""

    def __init__(self):
        self.data = self.load()
        self.session_history = []
        self.last_command = None
        self.last_topic = None
        self.last_action = None
        self.active_device = None
        self.user_patterns = defaultdict(int)
        self.pending_confirmation = None

    def load(self):
        if CONTEXT_FILE.exists():
            try:
                with open(CONTEXT_FILE, "r") as f:
                    data = json.load(f)
                # Ensure all required keys exist
                defaults = {
                    "command_frequency": {},
                    "successful_patterns": [],
                    "preferences": {},
                    "command_history": [],
                    "favorite_commands": [],
                    "device_preferences": {},
                    "music_preferences": {}
                }
                for key, default_value in defaults.items():
                    if key not in data:
                        data[key] = default_value
                return data
            except (json.JSONDecodeError, Exception):
                # If file is corrupted, return defaults
                return self._get_defaults()
        return self._get_defaults()

    def _get_defaults(self):
        """Return default context structure"""
        return {
            "command_frequency": {},
            "successful_patterns": [],
            "preferences": {},
            "command_history": [],
            "favorite_commands": [],
            "device_preferences": {},
            "music_preferences": {}
        }

    def save(self):
        """Save context with error handling"""
        try:
            # Ensure directory exists
            CONTEXT_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(CONTEXT_FILE, "w") as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            print(f"{Fore.YELLOW}⚠️  Could not save context: {e}{Style.RESET_ALL}")

    def record_command(self, cmd, args, success):
        """Record with enhanced pattern learning"""
        # Ensure command_history exists
        if "command_history" not in self.data:
            self.data["command_history"] = []
        if "successful_patterns" not in self.data:
            self.data["successful_patterns"] = []
        if "command_frequency" not in self.data:
            self.data["command_frequency"] = {}
        if "favorite_commands" not in self.data:
            self.data["favorite_commands"] = []

        entry = {
            "command": cmd,
            "args": args,
            "success": success,
            "timestamp": datetime.now().isoformat(),
            "context": self.last_topic,
            "action": self.last_action
        }
        self.data["command_history"].append(entry)
        self.data["command_history"] = self.data["command_history"][-100:]

        if success:
            pattern = f"{self.last_action}:{cmd}" if self.last_action else cmd
            self.data["successful_patterns"].append(pattern)

            # Track favorites
            freq = self.data["command_frequency"].get(cmd, 0) + 1
            self.data["command_frequency"][cmd] = freq

            if freq > 10 and cmd not in self.data["favorite_commands"]:
                self.data["favorite_commands"].append(cmd)

        self.last_command = cmd
        self.save()

    def get_likely_command(self, topic):
        """Predict with multi-signal approach"""
        candidates = []

        # Pattern-based
        patterns = [p for p in self.data["successful_patterns"] if topic in p]
        if patterns:
            cmds = [p.split(":")[-1] for p in patterns]
            candidates.append((max(set(cmds), key=cmds.count), 0.8))

        # Frequency-based
        if self.data["command_frequency"]:
            top = max(self.data["command_frequency"].items(), key=lambda x: x[1])
            candidates.append((top[0], 0.5))

        return candidates[0][0] if candidates else None

    def add_to_session(self, user_msg, bot_msg):
        """Session memory with context retention"""
        self.session_history.append({
            "user": user_msg,
            "bot": bot_msg,
            "time": datetime.now(),
            "command": self.last_command,
            "topic": self.last_topic
        })
        self.session_history = self.session_history[-30:]

    def get_context_clues(self):
        """Extract context from recent conversation"""
        if not self.session_history:
            return {}

        recent = self.session_history[-3:]
        clues = {
            "recent_commands": [h["command"] for h in recent if h["command"]],
            "recent_topics": [h["topic"] for h in recent if h["topic"]],
            "last_action": self.last_action
        }
        return clues

# ---------------------------
# Load scripts with deep parsing
# ---------------------------
script_context = {}
for file in SCRIPTS_DIR.glob("*.[ps][hy]*"):
    if file.name.startswith("."):
        continue
    info = ScriptParser.parse_script(file)
    info["categories"] = KnowledgeBase.categorize_command(info)
    script_context[file.stem] = info

context = ConversationContext()

# ---------------------------
# Advanced NLU Engine
# ---------------------------
class NLUEngine:
    """Natural Language Understanding with context awareness"""

    @staticmethod
    def parse(user_input, conversation_ctx):
        """Deep parsing with context and pronoun resolution"""
        text = user_input.lower().strip()
        words = text.split()

        # Resolve pronouns and references
        if any(w in text for w in ["it", "that", "same", "again"]):
            if conversation_ctx.last_command:
                text = text.replace("it", conversation_ctx.last_command)
                text = text.replace("that", conversation_ctx.last_command)

        entities = {
            "action": KnowledgeBase.extract_action(text),
            "commands": [],
            "parameters": [],
            "temporal": NLUEngine.extract_temporal(text),
            "category": None,
            "intensity": NLUEngine.extract_intensity(text),
            "question_type": NLUEngine.detect_question(text),
            "music_intent": NLUEngine.extract_music_intent(text),
            "raw_text": user_input
        }

        # Direct command detection
        for cmd_name, cmd_info in script_context.items():
            if cmd_name in text:
                entities["commands"].append(cmd_name)
                continue

            # Synonym matching
            if KnowledgeBase.find_synonyms(text, cmd_name):
                entities["commands"].append(cmd_name)
                continue

            # Tag matching
            for tag in cmd_info.get("tags", []):
                if tag.lower() in text:
                    entities["commands"].append(cmd_name)
                    break

        # Category detection
        if not entities["commands"]:
            for category, keywords in KnowledgeBase.SEMANTIC_GROUPS.items():
                if any(kw in text for kw in keywords):
                    entities["category"] = category
                    break

        # Parameter extraction
        entities["parameters"] = NLUEngine.extract_parameters(user_input, entities)

        return entities

    @staticmethod
    def extract_parameters(user_input, entities):
        """Smart parameter extraction"""
        params = []

        # Quoted strings
        params.extend(re.findall(r'"([^"]*)"', user_input))
        params.extend(re.findall(r"'([^']*)'", user_input))

        # Paths
        params.extend(re.findall(r'(/[^\s]+)', user_input))
        params.extend(re.findall(r'(~/[^\s]+)', user_input))

        # Numbers (volume, etc)
        numbers = re.findall(r'\b(\d+)\b', user_input)
        params.extend(numbers)

        # Song names without quotes
        if entities["music_intent"]:
            # Extract song name after keywords
            song_pattern = r'(?:play|song|track)\s+(.+?)(?:\s+on|\s+at|\s+volume|$)'
            match = re.search(song_pattern, user_input.lower())
            if match:
                song = match.group(1).strip()
                if song and song not in params:
                    params.append(song)

        return params

    @staticmethod
    def extract_music_intent(text):
        """Detect music-specific intents"""
        intents = {
            "play_song": any(w in text for w in ["play", "play song", "play track"]),
            "control": any(w in text for w in ["next", "skip", "pause", "stop", "previous", "back"]),
            "volume": any(w in text for w in ["volume", "vol", "louder", "quieter"]),
            "shuffle": "shuffle" in text or "random" in text,
            "playlist": "playlist" in text,
            "status": any(w in text for w in ["what's playing", "current song", "now playing"])
        }
        return intents if any(intents.values()) else None

    @staticmethod
    def extract_temporal(text):
        """Time-based intent detection"""
        if any(w in text for w in ["now", "immediately", "asap", "quick"]):
            return "immediate"
        if any(w in text for w in ["later", "schedule", "wait"]):
            return "delayed"
        if any(w in text for w in ["again", "repeat", "keep", "continuous"]):
            return "recurring"
        return None

    @staticmethod
    def extract_intensity(text):
        """Urgency detection"""
        urgent = ["urgent", "asap", "now", "quick", "fast", "immediately", "hurry"]
        if any(w in text for w in urgent):
            return "high"
        return "normal"

    @staticmethod
    def detect_question(text):
        """Identify question types"""
        if text.startswith("what"):
            return "what"
        if text.startswith("how"):
            return "how"
        if text.startswith("why"):
            return "why"
        if text.startswith("when"):
            return "when"
        if text.startswith("can"):
            return "capability"
        if "?" in text:
            return "general"
        return None

# ---------------------------
# Intelligent Reasoning Engine
# ---------------------------
class ReasoningEngine:
    """Multi-level reasoning with context awareness"""

    @staticmethod
    def find_best_match(entities, conversation_ctx):
        """Advanced matching with multiple strategies"""
        candidates = []

        # Direct command matches (highest priority)
        for cmd in entities["commands"]:
            if cmd in script_context:
                candidates.append((cmd, 1.0, "direct"))

        # Music-specific routing
        if entities["music_intent"]:
            if "music" in script_context:
                score = 0.95
                if entities["music_intent"]["control"]:
                    score = 1.0
                candidates.append(("music", score, "music_intent"))

        # Context-based prediction
        if not candidates and conversation_ctx.last_command:
            # If user says "again" or "do it", repeat last command
            if any(w in entities["raw_text"].lower() for w in ["again", "do it", "repeat", "same"]):
                candidates.append((conversation_ctx.last_command, 0.9, "repeat"))

        # Category-based matching
        if entities["category"] and not candidates:
            for cmd_name, cmd_info in script_context.items():
                if entities["category"] in cmd_info["categories"]:
                    freq = conversation_ctx.data["command_frequency"].get(cmd_name, 0)
                    score = 0.6 + (min(freq, 20) * 0.02)
                    candidates.append((cmd_name, score, "category"))

        # Action-based semantic search
        if not candidates:
            candidates.extend(ReasoningEngine.semantic_search(entities, conversation_ctx))

        # Sort by score
        if candidates:
            candidates.sort(key=lambda x: x[1], reverse=True)
            return candidates[0][0], candidates[0][2], candidates[0][1]

        return None, None, 0.0

    @staticmethod
    def semantic_search(entities, conversation_ctx):
        """Deep semantic search with learned patterns"""
        candidates = []
        action = entities["action"]

        for cmd_name, cmd_info in script_context.items():
            score = 0.0
            desc = cmd_info["desc"].lower()

            # Action alignment
            if action == "start" and any(w in desc for w in ["start", "launch", "play", "run"]):
                score += 0.4
            elif action == "stop" and any(w in desc for w in ["stop", "kill", "end", "disconnect"]):
                score += 0.4
            elif action == "show" and any(w in desc for w in ["show", "display", "info", "status"]):
                score += 0.4
            elif action == "connect" and any(w in desc for w in ["connect", "pair", "link"]):
                score += 0.4
            elif action == "sync" and any(w in desc for w in ["sync", "backup", "commit", "save"]):
                score += 0.4

            # Parameter compatibility
            if entities["parameters"] and cmd_info["args"]:
                score += 0.15

            # Favorite bonus
            if cmd_name in conversation_ctx.data.get("favorite_commands", []):
                score += 0.1

            # Recent usage bonus
            recent = conversation_ctx.get_context_clues()
            if cmd_name in recent.get("recent_commands", []):
                score += 0.1

            if score > 0.3:
                candidates.append((cmd_name, score, "semantic"))

        return candidates

    @staticmethod
    def plan_execution(entities, conversation_ctx):
        """Create intelligent execution plan"""
        cmd, method, confidence = ReasoningEngine.find_best_match(entities, conversation_ctx)

        if not cmd:
            return None

        plan = {
            "steps": [],
            "requires_confirmation": False,
            "estimated_risk": "low",
            "confidence": confidence,
            "method": method
        }

        # Handle music commands specially
        if cmd == "music":
            args = ReasoningEngine.build_music_args(entities, conversation_ctx)
        else:
            args = entities["parameters"]

        step = {
            "command": cmd,
            "args": args,
            "background": ReasoningEngine.should_run_background(cmd),
            "method": method,
            "confidence": confidence
        }

        plan["steps"].append(step)

        # Risk assessment
        dangerous = ["delete", "remove", "kill", "stop", "format", "rm", "disconnect"]
        if any(d in script_context[cmd]["desc"].lower() for d in dangerous):
            plan["estimated_risk"] = "medium"
            plan["requires_confirmation"] = confidence < 0.8

        return plan

    @staticmethod
    def build_music_args(entities, conversation_ctx):
        """Build music command arguments from natural language"""
        args = []
        intent = entities["music_intent"]

        if intent["control"]:
            action = entities["raw_text"].lower()
            if "next" in action or "skip" in action:
                args.append("next")
            elif "prev" in action or "back" in action:
                args.append("prev")
            elif "pause" in action or "stop" in action:
                args.append("pause")
            elif "play" in action and not intent["play_song"]:
                args.append("play")
            elif "shuffle" in action:
                args.append("shuffle")

        if intent["volume"] and entities["parameters"]:
            # Extract volume number
            for param in entities["parameters"]:
                if param.isdigit():
                    args.extend(["vol", param])
                    break

        if intent["play_song"] and entities["parameters"]:
            # Get song name
            for param in entities["parameters"]:
                if not param.isdigit() and "/" not in param:
                    args.append(param)
                    break

        if intent["status"]:
            args.append("--status")

        return args

    @staticmethod
    def should_run_background(cmd):
        """Determine background execution"""
        if not cmd:
            return False
        desc = script_context.get(cmd, {}).get("desc", "").lower()
        bg_keywords = ["music", "server", "monitor", "watch", "daemon", "service"]
        return any(kw in desc for kw in bg_keywords) or cmd == "music"

# ---------------------------
# Smart Response Generator
# ---------------------------
class ResponseGenerator:
    """Context-aware response generation"""

    @staticmethod
    def generate(user_input, conversation_ctx):
        """Main response generation with conversation awareness"""
        text = user_input.lower().strip()

        # Handle confirmation
        if conversation_ctx.pending_confirmation:
            if text in ["yes", "y", "ok", "sure", "confirm"]:
                plan = conversation_ctx.pending_confirmation
                conversation_ctx.pending_confirmation = None
                return ResponseGenerator.execute_plan(plan, conversation_ctx), "execute"
            elif text in ["no", "n", "cancel", "nevermind"]:
                conversation_ctx.pending_confirmation = None
                return "❌ Cancelled.", "cancel"

        # Exit commands
        if text in ["exit", "quit", "bye", "goodbye"]:
            return None, "exit"

        # Help system
        if text in ["help", "?", "commands"]:
            return ResponseGenerator.generate_help(), "help"

        if text.startswith("help "):
            cmd = text.replace("help ", "").strip()
            if cmd in script_context:
                return ResponseGenerator.format_detailed_help(cmd), "help"

        # Reset context if corrupted
        if text in ["reset", "reset context", "clear context"]:
            conversation_ctx.data = conversation_ctx._get_defaults()
            conversation_ctx.save()
            return "✅ Context reset successfully! Starting fresh.", "reset"

        # Analytics and meta queries
        if "most" in text and ("used" in text or "popular" in text or "frequent" in text):
            return ResponseGenerator.show_analytics(conversation_ctx), "analytics"

        if any(phrase in text for phrase in ["what can", "what do you", "capabilities", "what are you"]):
            return ResponseGenerator.explain_capabilities(), "info"

        if "history" in text or "recent" in text or "last" in text:
            return ResponseGenerator.show_history(conversation_ctx), "history"

        if "favorites" in text or "favourite" in text:
            return ResponseGenerator.show_favorites(conversation_ctx), "favorites"

        # Parse user intent
        entities = NLUEngine.parse(user_input, conversation_ctx)
        conversation_ctx.last_action = entities["action"]

        # Update topic
        if entities["category"]:
            conversation_ctx.last_topic = entities["category"]

        # Handle questions
        if entities["question_type"]:
            response = ResponseGenerator.handle_question(entities, conversation_ctx)
            if response:
                return response, "question"

        # Execute command
        plan = ReasoningEngine.plan_execution(entities, conversation_ctx)

        if not plan:
            return ResponseGenerator.no_match_response(entities, conversation_ctx), "no_match"

        # Low confidence - ask for confirmation
        if plan["confidence"] < 0.7:
            cmd = plan["steps"][0]["command"]
            return f"🤔 Did you mean '{cmd}'? (yes/no)", "clarify"

        # Requires confirmation
        if plan["requires_confirmation"]:
            cmd = plan["steps"][0]["command"]
            conversation_ctx.pending_confirmation = plan
            return f"⚠️  '{cmd}' will modify system state. Confirm? (yes/no)", "confirm"

        return ResponseGenerator.execute_plan(plan, conversation_ctx), "execute"

    @staticmethod
    def execute_plan(plan, conversation_ctx):
        """Execute with rich feedback"""
        results = []

        for step in plan["steps"]:
            cmd = step["command"]
            args = step["args"]

            # Show what we're doing
            if step["confidence"] < 0.9:
                confidence = "✓" if step["confidence"] > 0.8 else "~"
                results.append(f"{confidence} Running: {cmd} {' '.join(args)}")

            # Execute
            success, output = execute_command(cmd, args, step["background"])
            conversation_ctx.record_command(cmd, args, success)

            # Format output
            if success:
                if output and output != "Success":
                    results.append(output)
                elif step["background"]:
                    results.append(f"✅ {cmd} started in background")
                else:
                    results.append(f"✅ {cmd} completed")
            else:
                results.append(f"❌ {cmd} failed: {output}")

        return "\n".join(results)

    @staticmethod
    def handle_question(entities, conversation_ctx):
        """Answer questions intelligently"""
        text = entities["raw_text"].lower()

        # "What's playing" / music status
        if any(phrase in text for phrase in ["what's playing", "current song", "now playing"]):
            if "music" in script_context:
                return ResponseGenerator.execute_plan({
                    "steps": [{"command": "music", "args": ["--status"], "background": False, "confidence": 1.0}]
                }, conversation_ctx)

        # Command-specific questions
        if entities["commands"]:
            cmd = entities["commands"][0]
            if "how" in text:
                return ResponseGenerator.format_detailed_help(cmd)
            if "what" in text:
                info = script_context[cmd]
                return f"💡 {cmd}: {info['desc']}"

        return None

    @staticmethod
    def no_match_response(entities, conversation_ctx):
        """Smart fallback with helpful suggestions"""
        suggestions = []

        # Category-based suggestions
        if entities["category"]:
            cmds = [name for name, info in script_context.items()
                   if entities["category"] in info["categories"]]
            if cmds:
                suggestions.append(f"💡 {entities['category'].title()} commands: {', '.join(cmds[:3])}")

        # Action-based suggestions
        action = entities["action"]
        if action != "query":
            action_cmds = []
            for name, info in script_context.items():
                desc = info["desc"].lower()
                if action in desc or any(v in desc for v in KnowledgeBase.ACTION_VERBS.get(action, [])):
                    action_cmds.append(name)
            if action_cmds:
                suggestions.append(f"🔍 For '{action}': {', '.join(action_cmds[:3])}")

        # Favorites suggestion
        if conversation_ctx.data.get("favorite_commands"):
            faves = conversation_ctx.data["favorite_commands"][:3]
            suggestions.append(f"⭐ Your favorites: {', '.join(faves)}")

        if suggestions:
            return "\n".join(suggestions) + f"\n\n💬 Try: 'help' or describe what you want to do"

        return "❓ I'm not sure what you want.\n💡 Try:\n  • 'help' - see all commands\n  • 'what can you do?' - learn more\n  • Describe your task in plain English"

    @staticmethod
    def generate_help():
        """Beautiful categorized help"""
        categories = defaultdict(list)
        for name, info in script_context.items():
            for cat in info["categories"]:
                categories[cat].append((name, info["desc"]))

        output = [f"{Fore.CYAN}╔═══════════════════════════════════════╗{Style.RESET_ALL}"]
        output.append(f"{Fore.CYAN}║       📚 Available Commands           ║{Style.RESET_ALL}")
        output.append(f"{Fore.CYAN}╚═══════════════════════════════════════╝{Style.RESET_ALL}\n")

        for category, cmds in sorted(categories.items()):
            output.append(f"{Fore.YELLOW}▸ {category.upper()}{Style.RESET_ALL}")
            for cmd, desc in sorted(cmds):
                short_desc = desc[:55] + "..." if len(desc) > 55 else desc
                output.append(f"  {Fore.GREEN}•{Style.RESET_ALL} {cmd:12} - {short_desc}")
            output.append("")

        output.append(f"{Fore.CYAN}💬 Natural Language Examples:{Style.RESET_ALL}")
        output.append("  • 'play some music'")
        output.append("  • 'connect my airpods'")
        output.append("  • 'show system info'")
        output.append("  • 'commit my notes'")
        output.append("  • 'next song' or 'skip'")
        output.append(f"\n{Fore.CYAN}📖 For detailed help:{Style.RESET_ALL} 'help <command>'")

        return "\n".join(output)

    @staticmethod
    def format_detailed_help(cmd):
        """Comprehensive command help"""
        info = script_context[cmd]
        output = [f"\n{Fore.CYAN}╔{'═' * 50}╗{Style.RESET_ALL}"]
        output.append(f"{Fore.CYAN}║  {cmd.upper():^48}║{Style.RESET_ALL}")
        output.append(f"{Fore.CYAN}╚{'═' * 50}╝{Style.RESET_ALL}\n")
        output.append(f"📝 {info['desc']}\n")

        if info["args"]:
            output.append(f"{Fore.YELLOW}Arguments:{Style.RESET_ALL}")
            for arg in info["args"]:
                output.append(f"  • {arg}")
            output.append("")

        if info.get("flags"):
            output.append(f"{Fore.YELLOW}Flags:{Style.RESET_ALL}")
            for flag in info["flags"]:
                output.append(f"  • {flag}")
            output.append("")

        if info.get("subcommands"):
            output.append(f"{Fore.YELLOW}Subcommands:{Style.RESET_ALL}")
            for sub, desc in info["subcommands"].items():
                output.append(f"  • {sub}")
            output.append("")

        if info.get("tags"):
            output.append(f"{Fore.YELLOW}Tags:{Style.RESET_ALL} {', '.join(info['tags'])}\n")

        if info.get("examples"):
            output.append(f"{Fore.YELLOW}Examples:{Style.RESET_ALL}")
            for ex in info["examples"]:
                output.append(f"  $ {ex}")
            output.append("")

        # Add natural language examples
        output.append(f"{Fore.CYAN}💬 You can also say:{Style.RESET_ALL}")
        if cmd == "music":
            output.append("  • 'play bohemian rhapsody'")
            output.append("  • 'next song' or 'skip'")
            output.append("  • 'volume 80'")
            output.append("  • 'shuffle'")
        elif cmd == "airpods":
            output.append("  • 'connect airpods'")
            output.append("  • 'connect my headphones'")
        elif cmd == "sysinfo":
            output.append("  • 'show system info'")
            output.append("  • 'check my computer stats'")
        elif cmd == "notes":
            output.append("  • 'commit my notes'")
            output.append("  • 'sync notes'")
        else:
            output.append(f"  • 'run {cmd}'")

        return "\n".join(output)

    @staticmethod
    def show_analytics(conversation_ctx):
        """Detailed usage analytics"""
        freq = conversation_ctx.data["command_frequency"]
        if not freq:
            return "📊 No commands used yet."

        total = sum(freq.values())
        top = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:7]

        output = [f"{Fore.CYAN}╔═══════════════════════════════════════╗{Style.RESET_ALL}"]
        output.append(f"{Fore.CYAN}║      📊 Command Analytics             ║{Style.RESET_ALL}")
        output.append(f"{Fore.CYAN}╚═══════════════════════════════════════╝{Style.RESET_ALL}\n")
        output.append(f"Total commands executed: {Fore.GREEN}{total}{Style.RESET_ALL}\n")

        for cmd, count in top:
            pct = (count / total) * 100
            bar_length = int(pct / 3)
            bar = f"{Fore.GREEN}{'█' * bar_length}{Style.RESET_ALL}"
            output.append(f"  {cmd:12} {bar} {count:3} ({pct:5.1f}%)")

        return "\n".join(output)

    @staticmethod
    def show_history(conversation_ctx):
        """Recent command history"""
        history = conversation_ctx.data["command_history"][-15:]
        if not history:
            return "📜 No command history."

        output = [f"{Fore.CYAN}📜 Recent Commands:{Style.RESET_ALL}\n"]
        for entry in reversed(history):
            time = datetime.fromisoformat(entry["timestamp"]).strftime("%H:%M")
            status = f"{Fore.GREEN}✓{Style.RESET_ALL}" if entry["success"] else f"{Fore.RED}✗{Style.RESET_ALL}"
            args_str = " ".join(entry["args"]) if entry["args"] else ""
            cmd_str = f"{entry['command']} {args_str}".strip()
            output.append(f"  {time} {status} {cmd_str}")

        return "\n".join(output)

    @staticmethod
    def show_favorites(conversation_ctx):
        """Show favorite commands"""
        faves = conversation_ctx.data.get("favorite_commands", [])
        if not faves:
            return "⭐ No favorites yet. Keep using commands to build your favorites list!"

        output = [f"{Fore.CYAN}⭐ Your Favorite Commands:{Style.RESET_ALL}\n"]
        for cmd in faves:
            info = script_context.get(cmd, {})
            desc = info.get("desc", "No description")
            count = conversation_ctx.data["command_frequency"].get(cmd, 0)
            output.append(f"  • {Fore.YELLOW}{cmd}{Style.RESET_ALL} ({count} uses)")
            output.append(f"    {desc}")

        return "\n".join(output)

    @staticmethod
    def explain_capabilities():
        """Explain what the bot can do"""
        return f"""{Fore.CYAN}╔═══════════════════════════════════════╗{Style.RESET_ALL}
{Fore.CYAN}║    🤖 Intelligent Command Assistant  ║{Style.RESET_ALL}
{Fore.CYAN}╚═══════════════════════════════════════╝{Style.RESET_ALL}

{Fore.GREEN}✅ Natural Language Understanding{Style.RESET_ALL}
   • "play bohemian rhapsody" → Plays song on Spotify
   • "next song" or just "skip" → Controls playback
   • "connect airpods" → Pairs Bluetooth devices
   • "show system info" → Displays hardware stats

{Fore.GREEN}✅ Smart Context Awareness{Style.RESET_ALL}
   • Remembers your last commands
   • "do it again" → Repeats last action
   • Learns your patterns and preferences
   • Suggests based on usage history

{Fore.GREEN}✅ Multi-Script Integration{Style.RESET_ALL}
   • {len(script_context)} commands loaded from ~/Scripts
   • Music control (Spotify CLI)
   • Bluetooth device management
   • System monitoring and SSH shortcuts
   • Note syncing and utilities

{Fore.GREEN}✅ Intelligent Features{Style.RESET_ALL}
   • Fuzzy matching & synonym understanding
   • Category-based command discovery
   • Safety confirmations for risky operations
   • Background process management
   • Usage analytics and favorites

{Fore.CYAN}💡 Try saying:{Style.RESET_ALL}
   • "play some music" or "skip"
   • "connect my headphones"
   • "what are my most used commands?"
   • "show me my favorites"
   • "commit notes" or "sync notes"

Type 'help' to see all available commands!"""

# ---------------------------
# Command Execution
# ---------------------------
def execute_command(cmd_name, args, background=False):
    """Execute with enhanced error handling"""
    cmd_info = script_context.get(cmd_name)
    if not cmd_info or not cmd_info["path"].exists():
        return False, f"Command '{JY_PREFIX}{cmd_name}' not found. Run 'jyupdate' to install."

    cmd_args = [str(cmd_info["path"])] + (args or [])

    try:
        if background:
            subprocess.Popen(
                cmd_args,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
            return True, "Started in background"
        else:
            result = subprocess.run(
                cmd_args,
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                output = result.stdout.strip()
                return True, output if output else "✓ Success"
            else:
                error = result.stderr.strip()
                return False, error if error else "Command failed"
    except subprocess.TimeoutExpired:
        return False, "⏱️  Command timed out (30s limit)"
    except FileNotFoundError:
        return False, f"Command not found. Try 'jyupdate' to install."
    except Exception as e:
        return False, f"Error: {str(e)}"

# ---------------------------
# Main Loop
# ---------------------------
def main():
    """Main conversation loop"""
    # Welcome message
    print(f"\n{Fore.CYAN}╔═══════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║   🤖 Intelligent jy Assistant        ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║   {len(script_context)} commands · AI-powered         ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚═══════════════════════════════════════╝{Style.RESET_ALL}")

    # Show quick stats
    if context.data["command_frequency"]:
        total_cmds = sum(context.data["command_frequency"].values())
        top_cmd = max(context.data["command_frequency"].items(), key=lambda x: x[1])
        print(f"{Fore.GREEN}📊 Session stats: {total_cmds} commands run · Top: {top_cmd[0]} ({top_cmd[1]}x){Style.RESET_ALL}")

    print(f"\n{Fore.CYAN}💡 Just tell me what you want to do!{Style.RESET_ALL}")
    print(f"{Fore.CYAN}   Examples: 'play music', 'skip', 'connect airpods', 'system info'{Style.RESET_ALL}\n")

    while True:
        try:
            user_input = input(f"{Fore.GREEN}You:{Style.RESET_ALL} ").strip()

            if not user_input:
                continue

            # Generate response
            response, response_type = ResponseGenerator.generate(user_input, context)

            if response_type == "exit":
                total = sum(context.data["command_frequency"].values())
                print(f"\n{Fore.CYAN}👋 Goodbye!{Style.RESET_ALL}")
                print(f"{Fore.GREEN}📊 Session summary: {total} commands executed{Style.RESET_ALL}")
                if context.data.get("favorite_commands"):
                    print(f"{Fore.YELLOW}⭐ Favorites: {', '.join(context.data['favorite_commands'][:3])}{Style.RESET_ALL}")
                break

            # Display response
            print(f"{Fore.MAGENTA}Bot:{Style.RESET_ALL} {response}\n")

            # Update session
            context.add_to_session(user_input, response)

        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}⚠️  Interrupted. Type 'exit' to quit.{Style.RESET_ALL}")
            continue
        except Exception as e:
            print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"{Fore.RED}Fatal error: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
