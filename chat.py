#!/usr/bin/env python3
# DESC: Ultra-intelligent chat assistant with deep script understanding (maximum intelligence)
# TAG: chat, assistant, ai, helper, jy
"""
Maximum intelligence jy assistant:
  - Deep semantic understanding with word embeddings simulation
  - Intent classification with confidence scoring
  - Multi-step reasoning with dependency resolution
  - Behavioral learning from execution patterns
  - Advanced NLP: coreference resolution, entity extraction, context tracking
  - Intelligent parameter inference and validation
  - Proactive suggestions based on time/patterns/state
"""

from __future__ import annotations
import ast
import subprocess
import json
import re
import shlex
import sys
import os
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime
from colorama import init, Fore, Style
from difflib import SequenceMatcher, get_close_matches
from typing import Dict, List, Tuple, Optional, Set

init(autoreset=True)

# ---------------------------
# Configuration
# ---------------------------
SCRIPTS_DIR = Path.home() / "Scripts"
BIN_DIR = Path("/usr/local/bin")
HISTORY_FILE = Path.home() / ".jychat_history"
CONTEXT_FILE = Path.home() / ".jychat_context.json"
JY_PREFIX = "jy"
MAX_HISTORY = 200
EXEC_TIMEOUT = 45

# ---------------------------
# Semantic Understanding Engine
# ---------------------------
class SemanticEngine:
    """Simulates semantic understanding using word relationships and patterns"""

    # Word embeddings simulation - related concepts
    SEMANTIC_CLUSTERS = {
        # Music/Audio cluster
        "music": {"play", "song", "track", "tune", "audio", "spotify", "listen", "sound", "melody", "album", "artist"},
        "control": {"next", "skip", "previous", "back", "pause", "stop", "resume", "forward", "rewind"},
        "volume": {"volume", "loud", "quiet", "louder", "quieter", "mute", "unmute", "vol"},
        "playlist": {"playlist", "queue", "list", "collection", "mix"},

        # Bluetooth/Connection cluster
        "bluetooth": {"bluetooth", "bt", "wireless", "pair", "pairing", "device"},
        "airpods": {"airpods", "headphones", "earbuds", "earphones", "buds", "pods"},
        "connect": {"connect", "pair", "link", "attach", "join", "sync"},
        "disconnect": {"disconnect", "unpair", "detach", "separate"},
        "battery": {"battery", "charge", "power", "percentage"},

        # System/Info cluster
        "system": {"system", "computer", "machine", "pc", "laptop"},
        "info": {"info", "information", "stats", "statistics", "status", "details"},
        "hardware": {"cpu", "ram", "memory", "disk", "gpu", "processor", "storage"},
        "network": {"network", "internet", "connection", "wifi", "ip", "address"},

        # File operations cluster
        "notes": {"notes", "note", "writing", "text", "document", "docs"},
        "git": {"git", "commit", "push", "pull", "version", "repository", "repo"},
        "save": {"save", "commit", "push", "sync", "backup", "store"},
        "file": {"file", "folder", "directory", "path"},

        # Actions cluster
        "show": {"show", "display", "view", "see", "list", "print", "get", "check"},
        "run": {"run", "execute", "start", "launch", "open", "begin"},
        "stop": {"stop", "end", "kill", "terminate", "close", "quit"},
        "change": {"change", "modify", "update", "edit", "set", "configure", "adjust"},

        # SSH/Remote cluster
        "ssh": {"ssh", "remote", "server", "host", "terminal", "shell"},
        "connect_remote": {"connect", "login", "access"},

        # Time/Scheduling cluster
        "time": {"time", "clock", "hour", "minute", "when"},
        "schedule": {"schedule", "timer", "alarm", "reminder", "cron"},

        # Utility cluster
        "utility": {"utility", "tool", "helper", "utils", "util"},
        "clear": {"clear", "clean", "wipe", "erase"},
        "echo": {"echo", "print", "output", "say"},
    }

    # Intent patterns with confidence weights
    INTENT_PATTERNS = {
        "execute": {
            "patterns": [r"\b(run|execute|start|launch|do|perform)\b", r"^(play|open|begin)"],
            "weight": 1.0
        },
        "query": {
            "patterns": [r"^(what|how|why|when|where|who)", r"\b(show|display|tell|check|get)\b"],
            "weight": 0.9
        },
        "control": {
            "patterns": [r"\b(next|skip|pause|stop|resume|previous|back|forward)\b"],
            "weight": 1.0
        },
        "configure": {
            "patterns": [r"\b(set|change|configure|adjust|modify)\b"],
            "weight": 0.85
        },
        "connect": {
            "patterns": [r"\b(connect|pair|link|join)\b"],
            "weight": 0.95
        },
    }

    @staticmethod
    def get_semantic_similarity(word1: str, word2: str) -> float:
        """Calculate semantic similarity between two words"""
        word1, word2 = word1.lower(), word2.lower()

        # Exact match
        if word1 == word2:
            return 1.0

        # Check if words share a semantic cluster
        for cluster_words in SemanticEngine.SEMANTIC_CLUSTERS.values():
            if word1 in cluster_words and word2 in cluster_words:
                return 0.85

        # Substring relationship
        if word1 in word2 or word2 in word1:
            return 0.7

        # Edit distance similarity
        return SequenceMatcher(None, word1, word2).ratio() * 0.6

    @staticmethod
    def extract_intent(text: str) -> Tuple[str, float]:
        """Extract intent with confidence score"""
        best_intent = "query"
        best_confidence = 0.5

        for intent, config in SemanticEngine.INTENT_PATTERNS.items():
            for pattern in config["patterns"]:
                if re.search(pattern, text, re.IGNORECASE):
                    confidence = config["weight"]
                    if confidence > best_confidence:
                        best_intent = intent
                        best_confidence = confidence

        return best_intent, best_confidence

    @staticmethod
    def find_semantic_matches(query_words: Set[str], target_words: Set[str]) -> float:
        """Find semantic matches between two word sets"""
        if not query_words or not target_words:
            return 0.0

        total_score = 0.0
        for qword in query_words:
            best_match = max(
                (SemanticEngine.get_semantic_similarity(qword, tword) for tword in target_words),
                default=0.0
            )
            total_score += best_match

        return total_score / len(query_words)

# ---------------------------
# Intelligent Script Analyzer
# ---------------------------
class ScriptAnalyzer:
    """Deep analysis of script functionality and behavior"""

    @staticmethod
    def analyze_script(file_path: Path) -> Dict:
        """Comprehensive script analysis"""
        text = file_path.read_text(encoding="utf-8", errors="ignore")
        lines = text.splitlines()

        metadata = {
            "type": "py" if file_path.suffix == ".py" else "sh",
            "desc": "",
            "args": [],
            "tags": [],
            "examples": [],
            "flags": [],
            "subcommands": {},
            "path": None,
            "name": file_path.stem,
            "filename": str(file_path),

            # Enhanced analysis
            "behavior": ScriptAnalyzer._analyze_behavior(text, file_path.suffix),
            "dependencies": ScriptAnalyzer._extract_dependencies(text),
            "side_effects": ScriptAnalyzer._detect_side_effects(text),
            "input_types": ScriptAnalyzer._infer_input_types(text),
            "output_format": ScriptAnalyzer._infer_output_format(text),
            "keywords": set(),
            "action_verbs": set(),
            "entities": set(),
        }

        # Extract metadata comments
        for line in lines:
            s = line.strip()
            if s.startswith("# DESC:"):
                metadata["desc"] = s.split(":", 1)[1].strip()
            elif s.startswith("# ARG:"):
                metadata["args"].append(s.split(":", 1)[1].strip())
            elif s.startswith("# TAG:"):
                metadata["tags"].extend([t.strip() for t in s.split(":", 1)[1].split(",") if t.strip()])
            elif s.startswith("# EXAMPLE:"):
                metadata["examples"].append(s.split(":", 1)[1].strip())

        # Parse structure
        if metadata["type"] == "py":
            ScriptAnalyzer._parse_python(text, metadata)
        else:
            ScriptAnalyzer._parse_bash(text, metadata)

        # Extract keywords from all text
        metadata["keywords"] = ScriptAnalyzer._extract_keywords(text, metadata)
        metadata["action_verbs"] = ScriptAnalyzer._extract_action_verbs(text)
        metadata["entities"] = ScriptAnalyzer._extract_entities(text, metadata)

        return metadata

    @staticmethod
    def _analyze_behavior(text: str, suffix: str) -> Dict:
        """Analyze what the script actually does"""
        behavior = {
            "is_interactive": False,
            "is_long_running": False,
            "modifies_files": False,
            "network_access": False,
            "system_changes": False,
            "background_suitable": False,
        }

        # Interactive indicators
        if re.search(r'\binput\(|raw_input\(|read\s+-p', text):
            behavior["is_interactive"] = True

        # Long running indicators
        if re.search(r'\bwhile\s+True|while\s+\d+|for\s+i\s+in\s+range\(\d{3,}', text):
            behavior["is_long_running"] = True

        # File modifications
        if re.search(r'\bopen\([^)]+["\']w["\']|write\(|>>|touch\s+|rm\s+|mv\s+', text):
            behavior["modifies_files"] = True

        # Network access
        if re.search(r'\brequests\.|urllib|curl|wget|http|api|fetch', text, re.IGNORECASE):
            behavior["network_access"] = True

        # System changes
        if re.search(r'\bsudo|systemctl|service|apt|yum|pacman|chmod|chown', text):
            behavior["system_changes"] = True

        # Background suitable (servers, monitors, music players)
        if re.search(r'\bserver|daemon|monitor|watch|music|stream|spotify', text, re.IGNORECASE):
            behavior["background_suitable"] = True

        return behavior

    @staticmethod
    def _extract_dependencies(text: str) -> List[str]:
        """Extract external dependencies"""
        deps = set()

        # Python imports
        for match in re.finditer(r'^\s*(?:import|from)\s+([a-zA-Z_][a-zA-Z0-9_\.]*)', text, re.MULTILINE):
            deps.add(match.group(1).split('.')[0])

        # Command executions
        for match in re.finditer(r'(?:subprocess|os\.system|Popen)\(["\']([a-z][a-z0-9_-]+)', text):
            deps.add(match.group(1))

        # Bash commands
        for match in re.finditer(r'(?:^|\||\$\()\s*([a-z][a-z0-9_-]+)\s+', text, re.MULTILINE):
            cmd = match.group(1)
            if cmd not in ["if", "then", "else", "fi", "do", "done", "for", "while", "case", "esac"]:
                deps.add(cmd)

        return sorted(deps)

    @staticmethod
    def _detect_side_effects(text: str) -> List[str]:
        """Detect potential side effects"""
        effects = []

        dangerous_patterns = {
            "file_deletion": r'\brm\s+-rf|shutil\.rmtree|os\.remove',
            "system_modification": r'\bsudo|apt|yum|systemctl',
            "network_modification": r'\biptables|firewall|ufw',
            "process_killing": r'\bkill\s+-9|pkill|killall',
        }

        for effect_name, pattern in dangerous_patterns.items():
            if re.search(pattern, text):
                effects.append(effect_name)

        return effects

    @staticmethod
    def _infer_input_types(text: str) -> List[str]:
        """Infer what types of inputs the script expects"""
        types = set()

        patterns = {
            "file_path": r'(?:path|file|dir|directory).*["\']?/|\.exists\(\)|Path\(',
            "url": r'https?://|url.*=',
            "number": r'int\(|float\(|\d+',
            "text": r'str\(|input\(|read.*line',
            "boolean": r'--.*flag|action=["\']store_true',
        }

        for input_type, pattern in patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                types.add(input_type)

        return sorted(types)

    @staticmethod
    def _infer_output_format(text: str) -> str:
        """Infer the output format"""
        if re.search(r'json\.dump|\.json\(', text):
            return "json"
        elif re.search(r'\.csv|DataFrame', text):
            return "csv"
        elif re.search(r'print.*table|tabulate', text):
            return "table"
        elif re.search(r'subprocess|Popen.*stdout', text):
            return "command_output"
        else:
            return "text"

    @staticmethod
    def _extract_keywords(text: str, metadata: Dict) -> Set[str]:
        """Extract meaningful keywords"""
        # Combine all text sources
        all_text = (
            metadata.get("desc", "") + " " +
            " ".join(metadata.get("tags", [])) + " " +
            " ".join(metadata.get("examples", [])) + " " +
            text[:2000]  # Sample of actual code
        )

        # Extract words
        words = re.findall(r'\b[a-z][a-z0-9_]{2,}\b', all_text.lower())

        # Filter stopwords
        stopwords = {"the", "and", "for", "with", "this", "that", "from", "have", "has", "will", "can", "are", "was", "were"}
        keywords = {w for w in words if w not in stopwords and len(w) > 2}

        return keywords

    @staticmethod
    def _extract_action_verbs(text: str) -> Set[str]:
        """Extract action verbs from script"""
        common_verbs = {
            "play", "stop", "pause", "start", "run", "execute", "connect", "disconnect",
            "show", "display", "print", "list", "get", "set", "update", "modify",
            "create", "delete", "remove", "add", "sync", "backup", "restore",
            "open", "close", "kill", "restart", "reload", "refresh"
        }

        found_verbs = set()
        for verb in common_verbs:
            if re.search(r'\b' + verb + r'\b', text, re.IGNORECASE):
                found_verbs.add(verb)

        return found_verbs

    @staticmethod
    def _extract_entities(text: str, metadata: Dict) -> Set[str]:
        """Extract named entities (proper nouns, services, etc.)"""
        entities = set()

        # Look for capitalized words (proper nouns)
        entities.update(re.findall(r'\b([A-Z][a-z]+(?:[A-Z][a-z]+)*)\b', text))

        # Common services
        services = ["Spotify", "Bluetooth", "Git", "SSH", "Docker", "systemd"]
        for service in services:
            if service.lower() in text.lower():
                entities.add(service)

        return entities

    @staticmethod
    def _parse_python(text: str, metadata: Dict):
        """Parse Python-specific structures"""
        try:
            tree = ast.parse(text)
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                    if node.func.attr == "add_argument":
                        name, help_text = None, None
                        for arg in node.args:
                            if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                                name = arg.value
                        for kw in node.keywords:
                            if kw.arg == "help" and isinstance(kw.value, ast.Constant):
                                help_text = kw.value.value
                        if name and help_text:
                            metadata["flags"].append(f"{name} - {help_text}")
        except:
            pass

    @staticmethod
    def _parse_bash(text: str, metadata: Dict):
        """Parse Bash-specific structures"""
        # Case statements
        for match in re.finditer(r'case\s+[^;]+in(.*?)esac', text, re.DOTALL):
            block = match.group(1)
            for opt in re.findall(r'([a-zA-Z0-9_-]+)\)', block):
                if opt not in ["*", "help"]:
                    metadata["subcommands"][opt] = f"Subcommand: {opt}"

# ---------------------------
# Context-Aware Conversation Manager
# ---------------------------
class ConversationManager:
    """Manages conversation state with deep context tracking"""

    def __init__(self):
        self.data = self._load()
        self.session_history = []
        self.last_command = None
        self.last_action = None
        self.conversation_state = "idle"
        self.pending_confirmation = None

    def _load(self) -> Dict:
        defaults = {
            "command_frequency": {},
            "successful_patterns": [],
            "command_history": [],
            "favorite_commands": [],
            "learned_associations": {},
            "time_patterns": {},
            "error_patterns": {},
        }

        if CONTEXT_FILE.exists():
            try:
                data = json.loads(CONTEXT_FILE.read_text())
                for k, v in defaults.items():
                    data.setdefault(k, v)
                return data
            except:
                return defaults
        return defaults

    def save(self):
        try:
            CONTEXT_FILE.parent.mkdir(parents=True, exist_ok=True)
            CONTEXT_FILE.write_text(json.dumps(self.data, indent=2))
        except Exception as e:
            print(f"{Fore.YELLOW}⚠️ Could not save context: {e}{Style.RESET_ALL}")

    def record_command(self, name: str, args: List[str], success: bool):
        """Record with behavioral learning"""
        entry = {
            "command": name,
            "args": args,
            "success": success,
            "timestamp": datetime.now().isoformat(),
            "action": self.last_action,
            "context": self.conversation_state,
        }

        self.data["command_history"].append(entry)
        self.data["command_history"] = self.data["command_history"][-MAX_HISTORY:]

        if success:
            # Learn patterns
            pattern = f"{self.last_action}:{name}" if self.last_action else name
            self.data["successful_patterns"].append(pattern)

            # Track frequency
            freq = self.data["command_frequency"]
            freq[name] = freq.get(name, 0) + 1

            # Learn associations
            if args:
                key = f"{name}:args"
                self.data.setdefault("learned_associations", {})[key] = args

            # Track time patterns
            hour = datetime.now().hour
            time_key = f"{name}:hour:{hour}"
            self.data.setdefault("time_patterns", {})[time_key] = \
                self.data["time_patterns"].get(time_key, 0) + 1

            # Update favorites
            if freq[name] > 8 and name not in self.data.get("favorite_commands", []):
                self.data["favorite_commands"].append(name)
        else:
            # Learn from errors
            error_key = f"{name}:{':'.join(args[:2])}"
            self.data.setdefault("error_patterns", {})[error_key] = \
                self.data["error_patterns"].get(error_key, 0) + 1

        self.last_command = name
        self.save()

    def get_contextual_suggestions(self) -> List[str]:
        """Get smart suggestions based on context"""
        suggestions = []
        hour = datetime.now().hour

        # Time-based suggestions
        time_patterns = self.data.get("time_patterns", {})
        for key, count in sorted(time_patterns.items(), key=lambda x: x[1], reverse=True):
            parts = key.split(":")
            if len(parts) == 3 and int(parts[2]) == hour and count > 2:
                cmd = parts[0]
                if cmd not in [e.get("command") for e in self.session_history[-3:]]:
                    suggestions.append(f"💡 You usually run '{cmd}' around this time")
                    break

        # Sequence suggestions
        if self.last_command:
            history = self.data.get("command_history", [])
            following_commands = Counter()
            for i, entry in enumerate(history[:-1]):
                if entry["command"] == self.last_command and i + 1 < len(history):
                    next_cmd = history[i + 1]["command"]
                    following_commands[next_cmd] += 1

            if following_commands:
                most_common = following_commands.most_common(1)[0]
                if most_common[1] > 2:
                    suggestions.append(f"💡 After '{self.last_command}', you usually run '{most_common[0]}'")

        return suggestions[:2]

    def update_state(self, new_state: str):
        """Update conversation state"""
        self.conversation_state = new_state

    def add_to_session(self, user: str, bot: str):
        """Add a turn to the short-term session history"""
        self.session_history.append({
            "user": user,
            "bot": bot,
            "time": datetime.now().isoformat(),
            "command": self.last_command
        })
        # Keep only the last 50 turns in session
        self.session_history = self.session_history[-50:]

    def resolve_reference(self, text: str) -> str:
        """Resolve references like 'it', 'that', 'the same'"""
        if any(word in text.lower() for word in ["it", "that", "this", "same"]):
            if self.last_command:
                text = re.sub(r'\b(it|that|this)\b', self.last_command, text, flags=re.IGNORECASE)
        return text

# ---------------------------
# Advanced NLU Engine
# ---------------------------
class AdvancedNLU:
    """Advanced Natural Language Understanding"""

    @staticmethod
    def parse(user_input: str, ctx: ConversationManager, scripts: Dict) -> Dict:
        """Deep NLU parsing with context"""
        # Resolve references
        text = ctx.resolve_reference(user_input)

        entities = {
            "raw_text": user_input,
            "resolved_text": text,
            "normalized": text.lower().strip(),
            "intent": None,
            "intent_confidence": 0.0,
            "commands": [],
            "command_scores": {},
            "parameters": [],
            "temporal": None,
            "modifiers": [],
        }

        # Extract intent
        entities["intent"], entities["intent_confidence"] = SemanticEngine.extract_intent(text)

        # Extract temporal information
        entities["temporal"] = AdvancedNLU._extract_temporal(text)

        # Extract modifiers
        entities["modifiers"] = AdvancedNLU._extract_modifiers(text)

        # Match commands using semantic understanding
        query_words = set(re.findall(r'\b[a-z][a-z0-9_]{2,}\b', entities["normalized"]))

        for cmd_name, cmd_info in scripts.items():
            score = AdvancedNLU._score_command(
                cmd_name, cmd_info, query_words, entities, ctx
            )

            if score > 0.3:
                entities["command_scores"][cmd_name] = score
                if score > 0.6:
                    entities["commands"].append(cmd_name)

        # Sort commands by score
        entities["commands"] = sorted(
            entities["commands"],
            key=lambda c: entities["command_scores"].get(c, 0),
            reverse=True
        )

        # Extract parameters intelligently
        if entities["commands"]:
            best_cmd = entities["commands"][0]
            entities["parameters"] = AdvancedNLU._extract_parameters(
                text, best_cmd, scripts.get(best_cmd, {})
            )

        return entities

    @staticmethod
    def _score_command(cmd_name: str, cmd_info: Dict, query_words: Set[str],
                       entities: Dict, ctx: ConversationManager) -> float:
        """Intelligent command scoring"""
        score = 0.0

        # 1. Exact name match
        if cmd_name in entities["normalized"]:
            score += 1.5

        # 2. Semantic similarity with keywords
        cmd_keywords = cmd_info.get("keywords", set())
        if cmd_keywords:
            semantic_score = SemanticEngine.find_semantic_matches(query_words, cmd_keywords)
            score += semantic_score * 1.2

        # 3. Action verb matching
        action_verbs = cmd_info.get("action_verbs", set())
        if action_verbs:
            for verb in action_verbs:
                if verb in entities["normalized"]:
                    score += 0.4

        # 4. Description similarity
        desc = cmd_info.get("desc", "").lower()
        if desc:
            desc_words = set(re.findall(r'\b[a-z][a-z0-9_]{2,}\b', desc))
            overlap = len(query_words & desc_words)
            score += overlap * 0.15

        # 5. Tags match
        for tag in cmd_info.get("tags", []):
            if tag.lower() in entities["normalized"]:
                score += 0.5

        # 6. Behavior matching
        behavior = cmd_info.get("behavior", {})
        if entities["intent"] == "query" and "show" in entities["normalized"]:
            if behavior.get("output_format") in ["text", "table"]:
                score += 0.3

        # 7. Frequency boost
        freq = ctx.data.get("command_frequency", {}).get(cmd_name, 0)
        score += min(freq * 0.05, 0.5)

        # 8. Recent usage boost
        recent = [e.get("command") for e in ctx.session_history[-5:]]
        if cmd_name in recent:
            score += 0.3

        # 9. Time pattern matching
        hour = datetime.now().hour
        time_key = f"{cmd_name}:hour:{hour}"
        if ctx.data.get("time_patterns", {}).get(time_key, 0) > 2:
            score += 0.2

        # 10. Entity matching
        entities_in_script = cmd_info.get("entities", set())
        if entities_in_script:
            for entity in entities_in_script:
                if entity.lower() in entities["normalized"]:
                    score += 0.4

        return score

    @staticmethod
    def _extract_parameters(text: str, cmd_name: str, cmd_info: Dict) -> List[str]:
        """Intelligently extract parameters"""
        # Remove command name
        clean_text = re.sub(r'\b' + re.escape(cmd_name) + r'\b', '', text, flags=re.IGNORECASE).strip()

        try:
            # Use shlex for proper parsing
            params = shlex.split(clean_text)
        except ValueError:
            # Fallback to simple split
            params = clean_text.split()

        # Filter out common words
        stopwords = {"the", "a", "an", "to", "for", "my", "some", "please"}
        params = [p for p in params if p.lower() not in stopwords]

        # Validate parameters
        input_types = cmd_info.get("input_types", [])
        if "file_path" in input_types:
            paths = re.findall(r'(?:~)?/[^\s]+', text)
            params.extend(paths)

        if "url" in input_types:
            urls = re.findall(r'https?://[^\s]+', text)
            params.extend(urls)

        return params

    @staticmethod
    def _extract_temporal(text: str) -> Optional[str]:
        """Extract temporal information"""
        if any(w in text for w in ["now", "immediately", "asap"]):
            return "immediate"
        if any(w in text for w in ["later", "schedule", "soon"]):
            return "delayed"
        if any(w in text for w in ["again", "repeat", "keep"]):
            return "recurring"
        return None

    @staticmethod
    def _extract_modifiers(text: str) -> List[str]:
        """Extract modifying words"""
        modifiers = []
        mod_patterns = {
            "urgency": r'\b(urgent|quick|fast|asap|now|immediately)\b',
            "quality": r'\b(best|good|better|optimal|perfect)\b',
            "quantity": r'\b(all|some|few|many|several)\b',
            "certainty": r'\b(maybe|perhaps|probably|definitely)\b',
        }

        for mod_type, pattern in mod_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                modifiers.append(mod_type)

        return modifiers

# ---------------------------
# Intelligent Reasoning
# ---------------------------
# Intelligent Reasoning Engine
# ---------------------------
class ReasoningEngine:
    """Multi-step reasoning with dependency resolution"""

    @staticmethod
    def create_execution_plan(entities: Dict, ctx: ConversationManager, scripts: Dict) -> Optional[Dict]:
        """Create intelligent execution plan"""

        if not entities["commands"]:
            return None

        # Multi-step detection
        conjunctions = r'\s+(and then|and|then|after that|followed by)\s+'
        segments = re.split(conjunctions, entities["resolved_text"], flags=re.IGNORECASE)

        # Filter out conjunction words
        command_segments = [s.strip() for s in segments if s.strip() and
                              not re.match(r'^(and then|and|then|after that|followed by)$', s.strip(), re.IGNORECASE)]

        plan = {
            "steps": [],
            "confidence": 1.0,
            "requires_confirmation": False,
            "risk_level": "low",
            "estimated_duration": 0,
        }

        if len(command_segments) > 1:
            # Multi-step plan
            for segment in command_segments:
                step_entities = AdvancedNLU.parse(segment, ctx, scripts)
                if step_entities["commands"]:
                    best_cmd = step_entities["commands"][0]
                    step = ReasoningEngine._create_step(
                        best_cmd, step_entities, scripts, ctx
                    )
                    plan["steps"].append(step)
                    plan["confidence"] = min(plan["confidence"], step["confidence"])
        elif entities["commands"]:
            # Single command
            best_cmd = entities["commands"][0]
            step = ReasoningEngine._create_step(best_cmd, entities, scripts, ctx)
            plan["steps"].append(step)
            plan["confidence"] = step["confidence"]
        else:
            return None # No commands found in any segment

        # Analyze plan
        plan = ReasoningEngine._analyze_plan(plan, ctx)

        return plan

    @staticmethod
    def _create_step(cmd_name: str, entities: Dict, scripts: Dict, ctx: ConversationManager) -> Dict:
        """Create a single execution step"""
        cmd_info = scripts.get(cmd_name, {})

        # Get parameters with intelligent inference
        params = entities["parameters"]

        # Check for learned associations
        learned_key = f"{cmd_name}:args"
        if not params and learned_key in ctx.data.get("learned_associations", {}):
            # Use previously learned params as suggestion
            learned_params = ctx.data["learned_associations"][learned_key]
            # Don't auto-apply, but note them for suggestion
            pass

        # Infer background execution
        behavior = cmd_info.get("behavior", {})
        should_background = behavior.get("background_suitable", False) and \
                            behavior.get("is_long_running", False)

        step = {
            "command": cmd_name,
            "args": params,
            "background": should_background,
            "confidence": entities["command_scores"].get(cmd_name, 0.5),
            "behavior": behavior,
            "dependencies": cmd_info.get("dependencies", []),
        }

        return step

    @staticmethod
    def _analyze_plan(plan: Dict, ctx: ConversationManager) -> Dict:
        """Analyze plan for risks and requirements"""

        total_risk = 0
        total_duration = 0

        for step in plan["steps"]:
            cmd_name = step["command"]
            cmd_info = script_context.get(cmd_name, {})

            # Check for side effects
            side_effects = cmd_info.get("side_effects", [])
            if side_effects:
                total_risk += len(side_effects) * 20
                plan["risk_level"] = "high" if total_risk > 50 else "medium"
                plan["requires_confirmation"] = True

            # Check past errors
            error_key = f"{cmd_name}:{':'.join(step['args'][:2])}"
            if ctx.data.get("error_patterns", {}).get(error_key, 0) > 2:
                plan["requires_confirmation"] = True
                step["warning"] = "This combination has failed before"

            # Estimate duration
            behavior = step.get("behavior", {})
            if behavior.get("is_long_running"):
                total_duration += 60
            elif behavior.get("network_access"):
                total_duration += 5
            else:
                total_duration += 1

        plan["estimated_duration"] = total_duration

        # Check dependencies between steps
        plan["dependency_chain"] = ReasoningEngine._check_dependencies(plan["steps"])

        return plan

    @staticmethod
    def _check_dependencies(steps: List[Dict]) -> List[str]:
        """Check if steps have dependency relationships"""
        deps = []
        for i, step in enumerate(steps):
            for j, other_step in enumerate(steps):
                if i != j:
                    # Check if step depends on other_step
                    step_deps = set(step.get("dependencies", []))
                    other_name = other_step["command"]
                    if other_name in step_deps:
                        deps.append(f"{other_name} → {step['command']}")
        return deps

# ---------------------------
# Response Generator with Intelligence
# ---------------------------
class IntelligentResponder:
    """Generate intelligent, context-aware responses"""

    @staticmethod
    def generate(user_input: str, ctx: ConversationManager) -> Tuple[str, str]:
        """Main response generation"""
        text = user_input.strip()
        normalized = text.lower()

        # Handle confirmations
        if ctx.pending_confirmation:
            if normalized in ("yes", "y", "confirm", "ok", "sure", "do it"):
                plan = ctx.pending_confirmation
                ctx.pending_confirmation = None
                ctx.update_state("executing")
                return IntelligentResponder._execute_plan(plan, ctx), "execute"
            elif normalized in ("no", "n", "cancel", "nevermind", "stop"):
                ctx.pending_confirmation = None
                ctx.update_state("idle")
                return "❌ Cancelled.", "cancel"

        # Meta commands
        if normalized in ("help", "?", "commands"):
            return IntelligentResponder._generate_help(), "help"

        if normalized.startswith("help "):
            cmd = normalized[5:].strip()
            if cmd in script_context:
                return IntelligentResponder._detailed_help(cmd), "help"

        if normalized in ("exit", "quit", "bye", "goodbye"):
            return None, "exit"

        if normalized in ("reset", "clear context"):
            ctx.data = ctx._load()
            ctx.save()
            return "✅ Context reset.", "reset"

        # Analytics
        if "most used" in normalized or "popular" in normalized:
            return IntelligentResponder._show_analytics(ctx), "analytics"

        if "history" in normalized or "recent" in normalized:
            return IntelligentResponder._show_history(ctx), "history"

        if "favorites" in normalized or "favourite" in normalized:
            return IntelligentResponder._show_favorites(ctx), "favorites"

        if "suggest" in normalized or "what should i" in normalized:
            return IntelligentResponder._show_suggestions(ctx), "suggestions"

        # Parse with advanced NLU
        ctx.update_state("parsing")
        entities = AdvancedNLU.parse(user_input, ctx, script_context)

        # Handle questions
        if any(normalized.startswith(q) for q in ["what", "how", "why", "when", "who"]):
            response = IntelligentResponder._handle_question(entities, ctx)
            if response:
                return response, "question"

        # Create execution plan
        ctx.update_state("reasoning")
        plan = ReasoningEngine.create_execution_plan(entities, ctx, script_context)

        if not plan:
            return IntelligentResponder._no_match_response(entities, ctx), "no_match"

        # Show suggestions if available
        suggestions = ctx.get_contextual_suggestions()
        suggestion_text = "\n" + "\n".join(suggestions) if suggestions else ""

        # Check confidence
        if plan["confidence"] < 0.55:
            ctx.pending_confirmation = plan
            cmd_list = ", ".join(f"'{s['command']}'" for s in plan["steps"])
            return f"🤔 I think you want: {cmd_list}\nConfidence: {plan['confidence']:.0%}\nIs this correct? (yes/no){suggestion_text}", "clarify"

        # Check if confirmation needed
        if plan["requires_confirmation"]:
            ctx.pending_confirmation = plan
            risk_msg = f" [Risk: {plan['risk_level']}]" if plan["risk_level"] != "low" else ""
            duration_msg = f" [~{plan['estimated_duration']}s]" if plan["estimated_duration"] > 10 else ""
            cmd_list = " → ".join(f"'{s['command']}'" for s in plan["steps"])

            warnings = []
            for step in plan["steps"]:
                if "warning" in step:
                    warnings.append(f"⚠️  {step['command']}: {step['warning']}")

            warning_text = "\n" + "\n".join(warnings) if warnings else ""

            return f"⚠️  Plan: {cmd_list}{risk_msg}{duration_msg}\n{warning_text}\nConfirm? (yes/no){suggestion_text}", "confirm"

        # Execute directly
        ctx.update_state("executing")
        result = IntelligentResponder._execute_plan(plan, ctx)
        ctx.update_state("idle")

        return result + suggestion_text, "execute"

    @staticmethod
    def _execute_plan(plan: Dict, ctx: ConversationManager) -> str:
        """Execute plan with rich feedback"""
        results = []

        for i, step in enumerate(plan["steps"]):
            cmd = step["command"]
            args = step["args"]

            # Show progress for multi-step
            if len(plan["steps"]) > 1:
                results.append(f"[{i+1}/{len(plan['steps'])}] Running {cmd}...")

            # Execute
            success, output = IntelligentResponder._execute_command(
                cmd, args, step.get("background", False)
            )

            ctx.record_command(cmd, args, success)

            # Format output
            if success:
                if output and output != "✓ Success":
                    results.append(output)
                elif step.get("background"):
                    results.append(f"✅ {cmd} started in background")
                else:
                    results.append(f"✅ {cmd} completed")
            else:
                results.append(f"❌ {cmd} failed: {output}")
                # Stop on failure for multi-step
                if len(plan["steps"]) > 1:
                    results.append("⚠️  Stopping execution due to failure")
                    break

        return "\n".join(results)

    @staticmethod
    def _execute_command(cmd_name: str, args: List[str], background: bool) -> Tuple[bool, str]:
        """Execute with enhanced error handling"""
        cmd_info = script_context.get(cmd_name)
        if not cmd_info:
            return False, "Command not found"

        path = cmd_info.get("path")
        if not path or not Path(path).exists():
            return False, f"Executable not found. Run 'jyupdate' to install."

        full_cmd = [str(path)] + args

        try:
            if background:
                subprocess.Popen(
                    full_cmd,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    start_new_session=True
                )
                return True, "Started in background"
            else:
                proc = subprocess.run(
                    full_cmd,
                    capture_output=True,
                    text=True,
                    timeout=EXEC_TIMEOUT
                )

                if proc.returncode == 0:
                    output = proc.stdout.strip()
                    return True, output if output else "✓ Success"
                else:
                    error = proc.stderr.strip()
                    return False, error if error else f"Exit code {proc.returncode}"

        except subprocess.TimeoutExpired:
            return False, f"⏱️  Timed out ({EXEC_TIMEOUT}s)"
        except Exception as e:
            return False, f"Error: {e}"

    @staticmethod
    def _handle_question(entities: Dict, ctx: ConversationManager) -> Optional[str]:
        """Answer questions intelligently"""
        text = entities["normalized"]

        # Status queries
        if any(phrase in text for phrase in ["what's playing", "now playing", "current song"]):
            if "music" in script_context:
                plan = {"steps": [{"command": "music", "args": ["--status"], "background": False}]}
                return IntelligentResponder._execute_plan(plan, ctx)

        # Command help
        if entities["commands"]:
            cmd = entities["commands"][0]
            if text.startswith("how"):
                return IntelligentResponder._detailed_help(cmd)
            if text.startswith("what"):
                info = script_context.get(cmd, {})
                return f"💡 {cmd}: {info.get('desc', 'No description')}"

        # General capabilities
        if "what can you do" in text or "capabilities" in text:
            return IntelligentResponder._explain_capabilities()

        return None

    @staticmethod
    def _no_match_response(entities: Dict, ctx: ConversationManager) -> str:
        """Intelligent fallback"""
        suggestions = []

        # Semantic suggestions based on query
        if entities["command_scores"]:
            top_matches = sorted(
                entities["command_scores"].items(),
                key=lambda x: x[1],
                reverse=True
            )[:3]

            if top_matches[0][1] > 0.25:  # Some relevance
                suggestions.append(
                    f"🔍 Did you mean: {', '.join(cmd for cmd, _ in top_matches)}?"
                )

        # Show favorites
        if ctx.data.get("favorite_commands"):
            faves = ctx.data["favorite_commands"][:3]
            suggestions.append(f"⭐ Your favorites: {', '.join(faves)}")

        # Contextual suggestions
        contextual = ctx.get_contextual_suggestions()
        suggestions.extend(contextual)

        if not suggestions:
            suggestions.append("💬 Try: 'help' to see all commands or describe what you want")

        return "\n".join(suggestions)

    @staticmethod
    def _generate_help() -> str:
        """Intelligent help generation"""
        lines = [f"{Fore.CYAN}╔═══════════════════════════════════╗{Style.RESET_ALL}"]
        lines.append(f"{Fore.CYAN}║     🤖 Available Commands      ║{Style.RESET_ALL}")
        lines.append(f"{Fore.CYAN}╚═══════════════════════════════════╝{Style.RESET_ALL}\n")

        # Group by category
        categories = defaultdict(list)
        for name, info in script_context.items():
            cats = info.get("categories", ["general"])
            for cat in cats:
                categories[cat].append((name, info.get("desc", "")))

        for cat in sorted(categories.keys()):
            lines.append(f"{Fore.YELLOW}▸ {cat.upper()}{Style.RESET_ALL}")
            for name, desc in sorted(categories[cat]):
                short_desc = desc[:50] + "..." if len(desc) > 50 else desc
                lines.append(f"  • {name:12} {short_desc}")
            lines.append("")

        lines.append(f"{Fore.CYAN}💡 Natural language examples:{Style.RESET_ALL}")
        lines.append("  • 'play bohemian rhapsody'")
        lines.append("  • 'connect airpods'")
        lines.append("  • 'show system info'")
        lines.append("  • 'commit notes and then show history'")

        return "\n".join(lines)

    @staticmethod
    def _detailed_help(cmd: str) -> str:
        """Detailed command help"""
        info = script_context.get(cmd, {})
        lines = [f"\n{Fore.CYAN}═══ {cmd.upper()} ═══{Style.RESET_ALL}"]
        lines.append(f"📝 {info.get('desc', 'No description')}\n")

        if info.get("flags"):
            lines.append(f"{Fore.YELLOW}Flags:{Style.RESET_ALL}")
            for flag in info["flags"]:
                lines.append(f"  • {flag}")
            lines.append("")

        if info.get("examples"):
            lines.append(f"{Fore.YELLOW}Examples:{Style.RESET_ALL}")
            for ex in info["examples"]:
                lines.append(f"  $ {ex}")
            lines.append("")

        behavior = info.get("behavior", {})
        if behavior:
            lines.append(f"{Fore.YELLOW}Behavior:{Style.RESET_ALL}")
            if behavior.get("is_interactive"):
                lines.append("  • Interactive (requires user input)")
            if behavior.get("network_access"):
                lines.append("  • Requires network access")
            if behavior.get("modifies_files"):
                lines.append("  • Modifies files")
            lines.append("")

        return "\n".join(lines)

    @staticmethod
    def _show_analytics(ctx: ConversationManager) -> str:
        """Show analytics"""
        freq = ctx.data.get("command_frequency", {})
        if not freq:
            return "📊 No commands used yet."

        total = sum(freq.values())
        top = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:7]

        lines = [f"{Fore.CYAN}📊 Command Analytics{Style.RESET_ALL}"]
        lines.append(f"Total executions: {total}\n")

        for cmd, count in top:
            pct = (count / total) * 100
            bar = "█" * int(pct / 5)
            lines.append(f"  {cmd:12} {bar} {count} ({pct:.1f}%)")

        return "\n".join(lines)

    @staticmethod
    def _show_history(ctx: ConversationManager) -> str:
        """Show history"""
        history = ctx.data.get("command_history", [])[-15:]
        if not history:
            return "📜 No history yet."

        lines = [f"{Fore.CYAN}📜 Recent Commands{Style.RESET_ALL}\n"]
        for entry in reversed(history):
            timestamp = datetime.fromisoformat(entry["timestamp"]).strftime("%H:%M")
            status = "✓" if entry["success"] else "✗"
            args_str = " ".join(entry.get("args", []))
            lines.append(f"  {timestamp} {status} {entry['command']} {args_str}")

        return "\n".join(lines)

    @staticmethod
    def _show_favorites(ctx: ConversationManager) -> str:
        """Show favorites"""
        faves = ctx.data.get("favorite_commands", [])
        if not faves:
            return "⭐ No favorites yet."

        lines = [f"{Fore.CYAN}⭐ Your Favorites{Style.RESET_ALL}\n"]
        for cmd in faves:
            freq = ctx.data["command_frequency"].get(cmd, 0)
            info = script_context.get(cmd, {})
            lines.append(f"  • {cmd} ({freq} uses)")
            lines.append(f"    {info.get('desc', '')}")

        return "\n".join(lines)

    @staticmethod
    def _show_suggestions(ctx: ConversationManager) -> str:
        """Show proactive suggestions"""
        suggestions = ctx.get_contextual_suggestions()

        if not suggestions:
            return "💡 No suggestions right now. Keep using commands and I'll learn your patterns!"

        return "\n".join(suggestions)

    @staticmethod
    def _explain_capabilities() -> str:
        """Explain capabilities"""
        return f"""{Fore.CYAN}🤖 Intelligent Command Assistant{Style.RESET_ALL}

{Fore.GREEN}✅ Natural Language Understanding{Style.RESET_ALL}
  • Semantic matching with context awareness
  • Multi-step command chains
  • Coreference resolution ("do it again")

{Fore.GREEN}✅ Behavioral Learning{Style.RESET_ALL}
  • Learns your usage patterns
  • Time-based suggestions
  • Error pattern avoidance
  • Favorite command tracking

{Fore.GREEN}✅ Intelligent Execution{Style.RESET_ALL}
  • Risk assessment and confirmation
  • Dependency resolution
  • Background process management
  • Parameter inference

{Fore.GREEN}✅ {len(script_context)} Commands Loaded{Style.RESET_ALL}
Type 'help' to see all commands!"""

# ---------------------------
# Script Context Builder
# ---------------------------
def build_script_context() -> Dict[str, Dict]:
    """Build enhanced script context"""
    context = {}

    if not SCRIPTS_DIR.exists():
        SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)

    for script_file in sorted(SCRIPTS_DIR.glob("*")):
        if script_file.name.startswith("."):
            continue

        if script_file.is_file() and script_file.suffix in [".py", ".sh", ""]:
            try:
                info = ScriptAnalyzer.analyze_script(script_file)

                # Resolve executable path
                candidates = [
                    BIN_DIR / (JY_PREFIX + info["name"]),
                    script_file,
                ]

                # --- START: NEW PERMISSION LOGIC ---
                resolved_path = None
                for candidate in candidates:
                    if candidate.exists() and candidate.is_file():
                        # Check if it's a system path (owned by root)
                        if candidate.parent == BIN_DIR:
                            if os.access(candidate, os.X_OK):
                                # It's in /usr/local/bin and already executable. Use it.
                                resolved_path = candidate
                                break
                            else:
                                # It's in /usr/local/bin but NOT executable.
                                # This is a broken symlink. Skip to the next candidate.
                                continue
                        else:
                            # It's a user script in ~/Scripts.
                            # We own it, so we CAN and SHOULD chmod it.
                            try:
                                candidate.chmod(candidate.stat().st_mode | 0o111)
                                resolved_path = candidate
                                break
                            except Exception as e:
                                print(f"{Fore.YELLOW}⚠️  Could not chmod {candidate.name}: {e}{Style.RESET_ALL}")
                                # Failed, but it's still the best path we have
                                resolved_path = candidate
                                break

                info["path"] = resolved_path or script_file # Fallback to script_file
                # --- END: NEW PERMISSION LOGIC ---

                # Categorize
                info["categories"] = categorize_script(info)

                context[info["name"]] = info
            except Exception as e:
                print(f"{Fore.YELLOW}⚠️  Error loading {script_file.name}: {e}{Style.RESET_ALL}")

    return context

def categorize_script(info: Dict) -> List[str]:
    """Categorize script"""
    text = (info.get("desc", "") + " " + " ".join(info.get("tags", []))).lower()
    keywords = info.get("keywords", set())

    categories = set()

    # Check against semantic clusters
    for cluster_name, cluster_words in SemanticEngine.SEMANTIC_CLUSTERS.items():
        if any(word in text or word in keywords for word in cluster_words):
            # Map cluster to category
            category_mapping = {
                "music": "media", "control": "media", "volume": "media", "playlist": "media",
                "bluetooth": "bluetooth", "airpods": "bluetooth", "connect": "network",
                "system": "system", "info": "system", "hardware": "system",
                "notes": "file_ops", "git": "file_ops", "save": "file_ops",
                "ssh": "network",
            }
            if cluster_name in category_mapping:
                categories.add(category_mapping[cluster_name])

    return sorted(categories) if categories else ["general"]

# ---------------------------
# Main
# ---------------------------
script_context = build_script_context()
context = ConversationManager()

def main():
    """Main conversation loop"""
    print(f"\n{Fore.CYAN}╔═══════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║    🤖 Intelligent jy Assistant      ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║    {len(script_context)} commands · Maximum AI       ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚═══════════════════════════════════════╝{Style.RESET_ALL}\n")

    # Show initial suggestions
    suggestions = context.get_contextual_suggestions()
    if suggestions:
        print(f"{Fore.YELLOW}💡 Suggestions:{Style.RESET_ALL}")
        for suggestion in suggestions:
            print(f"  {suggestion}")
        print()

    print("Type 'help' for commands, 'suggest' for ideas, 'exit' to quit.\n")

    try:
        while True:
            try:
                user_input = input(f"{Fore.GREEN}You:{Style.RESET_ALL} ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n👋 Goodbye!")
                break

            if not user_input:
                continue

            response, response_type = IntelligentResponder.generate(user_input, context)

            if response_type == "exit":
                total = sum(context.data.get("command_frequency", {}).values())
                print(f"\n{Fore.CYAN}👋 Goodbye!{Style.RESET_ALL}")
                print(f"{Fore.GREEN}📊 Session: {total} commands executed{Style.RESET_ALL}")
                break

            if response:
                print(f"{Fore.MAGENTA}Bot:{Style.RESET_ALL} {response}\n")

            context.add_to_session(user_input, response or "")

    except Exception as e:
        print(f"{Fore.RED}Fatal error: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
