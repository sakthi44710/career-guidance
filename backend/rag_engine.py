import os
import json
import requests
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from pypdf import PdfReader

load_dotenv()

class CareerAI:
    def __init__(self):
        self.hf_api_key = os.getenv("HUGGINGFACE_API_KEY")
        self.user_data: Dict[str, Dict] = {}
        
        # Multi-sector skill keywords
        self.skill_keywords = {
            # Technology & Engineering
            "tech": ["Python", "Java", "JavaScript", "React", "Node.js", "SQL", "AWS", "Docker", 
                     "Machine Learning", "Data Analysis", "HTML", "CSS", "Git", "Agile", "Scrum",
                     "TypeScript", "Angular", "Vue", "Django", "Flask", "TensorFlow", "Kubernetes",
                     "CI/CD", "Linux", "Azure", "MongoDB", "PostgreSQL", "REST API", "GraphQL"],
            
            # Healthcare & Medical
            "medical": ["Patient Care", "Clinical Skills", "Medical Diagnosis", "Treatment Planning",
                       "EMR/EHR", "HIPAA Compliance", "Medical Terminology", "Pharmacology",
                       "Anatomy", "Physiology", "CPR Certified", "BLS", "ACLS", "First Aid",
                       "Infection Control", "Vital Signs", "Patient Assessment", "Documentation",
                       "Medical Ethics", "Healthcare Management", "Telemedicine", "Surgery Assist"],
            
            # Nursing
            "nursing": ["Patient Care", "Medication Administration", "IV Therapy", "Wound Care",
                       "Patient Education", "Care Planning", "Nursing Assessment", "Critical Care",
                       "Pediatric Care", "Geriatric Care", "Mental Health", "Emergency Care",
                       "Hospice Care", "Rehabilitation", "Nursing Documentation", "Team Coordination"],
            
            # Physiotherapy
            "physio": ["Physical Assessment", "Therapeutic Exercise", "Manual Therapy", "Electrotherapy",
                      "Rehabilitation", "Pain Management", "Sports Injury", "Orthopedic Care",
                      "Neurological Rehab", "Cardiopulmonary Rehab", "Patient Education",
                      "Treatment Planning", "Mobility Training", "Posture Correction"],
            
            # Business & Management
            "business": ["Project Management", "Leadership", "Communication", "Strategic Planning",
                        "Financial Analysis", "Marketing", "Sales", "Business Development",
                        "Negotiation", "Presentation", "Excel", "PowerPoint", "Data Analysis",
                        "Budget Management", "Team Management", "Problem Solving", "CRM"],
            
            # Education
            "education": ["Teaching", "Curriculum Development", "Lesson Planning", "Classroom Management",
                         "Student Assessment", "Educational Technology", "Special Education",
                         "Communication", "Mentoring", "Research", "Subject Expertise"],
            
            # General/Soft Skills
            "general": ["Communication", "Teamwork", "Problem Solving", "Leadership", "Time Management",
                       "Critical Thinking", "Adaptability", "Attention to Detail", "Organization",
                       "Interpersonal Skills", "Research", "Documentation", "Presentation"]
        }
        
        # Role-specific requirements mapping
        self.role_requirements = {
            # Medical
            "doctor": ["Clinical Skills", "Medical Diagnosis", "Patient Care", "Treatment Planning", "Medical Ethics"],
            "physician": ["Clinical Skills", "Medical Diagnosis", "Patient Care", "Treatment Planning", "Research"],
            "mbbs": ["Clinical Skills", "Medical Diagnosis", "Anatomy", "Physiology", "Pharmacology"],
            "surgeon": ["Surgery Assist", "Clinical Skills", "Patient Care", "Precision", "Decision Making"],
            
            # Nursing
            "nurse": ["Patient Care", "Medication Administration", "Nursing Assessment", "Documentation", "Team Coordination"],
            "registered nurse": ["Patient Care", "Critical Care", "IV Therapy", "Care Planning", "Emergency Care"],
            "nursing": ["Patient Care", "Wound Care", "Vital Signs", "Patient Education", "Healthcare Management"],
            
            # Physiotherapy
            "physiotherapist": ["Physical Assessment", "Therapeutic Exercise", "Manual Therapy", "Rehabilitation", "Patient Education"],
            "physio": ["Physical Assessment", "Therapeutic Exercise", "Pain Management", "Mobility Training", "Treatment Planning"],
            "physical therapist": ["Physical Assessment", "Manual Therapy", "Sports Injury", "Neurological Rehab", "Patient Care"],
            
            # Technology
            "software engineer": ["Python", "Java", "Git", "Docker", "AWS", "Problem Solving"],
            "data scientist": ["Python", "Machine Learning", "TensorFlow", "SQL", "Data Analysis"],
            "data analyst": ["Python", "SQL", "Excel", "Data Analysis", "Visualization"],
            "frontend developer": ["JavaScript", "React", "HTML", "CSS", "TypeScript"],
            "backend developer": ["Python", "Node.js", "SQL", "REST API", "Docker"],
            "full stack developer": ["JavaScript", "React", "Node.js", "SQL", "Docker"],
            "devops engineer": ["Docker", "Kubernetes", "CI/CD", "AWS", "Linux"],
            "web developer": ["HTML", "CSS", "JavaScript", "React", "Git"],
            
            # Business
            "product manager": ["Agile", "Scrum", "Communication", "Leadership", "Data Analysis"],
            "business analyst": ["Data Analysis", "Excel", "Communication", "Problem Solving", "Documentation"],
            "project manager": ["Project Management", "Leadership", "Communication", "Agile", "Budget Management"],
            "marketing manager": ["Marketing", "Communication", "Data Analysis", "Strategy", "Leadership"],
            
            # Education
            "teacher": ["Teaching", "Lesson Planning", "Classroom Management", "Communication", "Student Assessment"],
            "professor": ["Teaching", "Research", "Curriculum Development", "Subject Expertise", "Mentoring"],
            
            # Default
            "default": ["Communication", "Problem Solving", "Teamwork", "Leadership", "Time Management"]
        }
        
        # Test API
        self.api_working = self._test_api()

    def _test_api(self) -> bool:
        if not self.hf_api_key:
            return False
        try:
            url = "https://huggingface.co/api/whoami-v2"
            resp = requests.get(url, headers={"Authorization": f"Bearer {self.hf_api_key}"}, timeout=10)
            return resp.status_code == 200
        except:
            return False

    def _call_llm(self, prompt: str, max_tokens: int = 256) -> str:
        return ""  # Using fallback mode

    def process_pdf(self, file_path: str):
        """Extract text from PDF using pypdf"""
        reader = PdfReader(file_path)
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text() + "\n"
        # Simple chunking by splitting into paragraphs
        chunks = [chunk.strip() for chunk in full_text.split("\n\n") if chunk.strip()]
        return full_text, chunks

    def _detect_sector(self, text: str, target_role: str) -> str:
        """Detect which sector the resume/role belongs to"""
        text_lower = text.lower() + " " + target_role.lower()
        
        # Medical indicators
        medical_terms = ["patient", "hospital", "clinic", "medical", "healthcare", "doctor", 
                        "physician", "surgery", "diagnosis", "treatment", "mbbs", "md"]
        nursing_terms = ["nurse", "nursing", "rn", "bsc nursing", "patient care", "medication"]
        physio_terms = ["physiotherapy", "physio", "physical therapy", "rehabilitation", "therapy"]
        tech_terms = ["software", "developer", "programming", "engineer", "data", "code", "web", "app"]
        business_terms = ["manager", "business", "marketing", "sales", "finance", "mba"]
        education_terms = ["teacher", "professor", "education", "teaching", "school", "college"]
        
        if any(term in text_lower for term in nursing_terms):
            return "nursing"
        elif any(term in text_lower for term in physio_terms):
            return "physio"
        elif any(term in text_lower for term in medical_terms):
            return "medical"
        elif any(term in text_lower for term in tech_terms):
            return "tech"
        elif any(term in text_lower for term in education_terms):
            return "education"
        elif any(term in text_lower for term in business_terms):
            return "business"
        return "general"

    def _extract_skills_from_text(self, text: str, sector: str) -> List[str]:
        """Extract skills based on detected sector"""
        found = []
        text_lower = text.lower()
        
        # Check sector-specific skills
        sector_skills = self.skill_keywords.get(sector, [])
        for skill in sector_skills:
            if skill.lower() in text_lower:
                found.append(skill)
        
        # Also check general skills
        for skill in self.skill_keywords["general"]:
            if skill.lower() in text_lower and skill not in found:
                found.append(skill)
        
        return found[:12] if found else ["Communication", "Teamwork", "Problem Solving"]

    def _get_missing_skills(self, current_skills: List[str], target_role: str) -> List[str]:
        """Determine missing skills based on target role"""
        role_key = target_role.lower()
        required = None
        
        for key in self.role_requirements:
            if key in role_key:
                required = self.role_requirements[key]
                break
        
        if not required:
            required = self.role_requirements["default"]
        
        missing = [s for s in required if s not in current_skills]
        
        if not missing:
            # Suggest advanced skills
            missing = [f"Advanced {required[0]}", f"Specialized {required[1]}"]
        
        return missing

    def calculate_ats_score(self, resume_text: str, target_role: str) -> int:
        """Calculate ATS score based on content analysis"""
        score = 50  # Base score
        sector = self._detect_sector(resume_text, target_role)
        
        # Check for key resume sections
        sections = ["experience", "education", "skills", "summary", "objective", "qualification", "training"]
        for section in sections:
            if section in resume_text.lower():
                score += 4
        
        # Check for quantifiable achievements
        if any(char.isdigit() for char in resume_text):
            score += 8
        
        # Check for role-relevant keywords
        role_words = target_role.lower().split()
        for word in role_words:
            if word in resume_text.lower() and len(word) > 3:
                score += 4
        
        # Check for sector-specific keywords
        sector_skills = self.skill_keywords.get(sector, [])
        matches = sum(1 for skill in sector_skills if skill.lower() in resume_text.lower())
        score += min(15, matches * 3)
        
        # Check resume length
        word_count = len(resume_text.split())
        if 300 <= word_count <= 1000:
            score += 8
        elif word_count > 1000:
            score += 4
        
        return min(95, max(35, score))

    def analyze_resume(self, file_path: str, target_role: str, user_id: str = None) -> Dict:
        """Analyze resume, extract skills, and auto-generate personalized roadmap"""
        try:
            full_text, chunks = self.process_pdf(file_path)
            
            # Detect sector
            sector = self._detect_sector(full_text, target_role)
            
            # Calculate ATS score
            ats_score = self.calculate_ats_score(full_text, target_role)
            
            # Extract skills
            skills_have = self._extract_skills_from_text(full_text, sector)
            skills_need = self._get_missing_skills(skills_have, target_role)
            
            # Auto-generate personalized roadmap based on skills needed
            roadmap = self.generate_roadmap(skills_need, target_role)
            
            # Store everything for user session (including roadmap)
            if user_id:
                self.user_data[user_id] = {
                    "resume_text": full_text,
                    "target_role": target_role,
                    "sector": sector,
                    "skills_have": skills_have,
                    "skills_need": skills_need,
                    "roadmap": roadmap,
                    "roadmap_goal": target_role
                }
            
            return {
                "ats_score": ats_score,
                "skills_you_have": skills_have,
                "skills_you_need": skills_need,
                "resume_content": full_text,
                "roadmap": roadmap
            }
        except Exception as e:
            print(f"Resume analysis error: {e}")
            return {"ats_score": 0, "skills_you_have": [], "skills_you_need": [], "resume_content": "", "roadmap": {}}

    def generate_roadmap(self, skills_to_learn: List[str], goal: str = "") -> Dict:
        """Generate a learning roadmap for any sector"""
        if not skills_to_learn:
            skills_to_learn = ["Professional Development"]
        
        # Detect sector from goal or skills
        goal_lower = goal.lower() if goal else ""
        
        # Learning resources by sector
        resources_map = {
            # Medical
            "Patient Care": ["Clinical Training", "Patient Communication Course", "Healthcare Ethics"],
            "Clinical Skills": ["Clinical Practice", "Medical Simulations", "Hospital Internship"],
            "Medical Diagnosis": ["Diagnostic Training", "Case Studies", "Clinical Rotations"],
            
            # Nursing
            "Medication Administration": ["Pharmacology Course", "Clinical Practice", "Safety Training"],
            "Nursing Assessment": ["Assessment Techniques", "Patient Evaluation", "Documentation Training"],
            
            # Physiotherapy
            "Physical Assessment": ["Assessment Courses", "Anatomy Study", "Practice Sessions"],
            "Therapeutic Exercise": ["Exercise Therapy Course", "Rehabilitation Training", "Sports Medicine"],
            "Manual Therapy": ["Hands-on Training", "Technique Workshops", "Clinical Practice"],
            
            # Technology
            "Python": ["Python.org Tutorial", "Codecademy Python", "Automate the Boring Stuff"],
            "JavaScript": ["MDN Web Docs", "freeCodeCamp JS", "JavaScript.info"],
            "React": ["React Official Docs", "Scrimba React", "Build Projects"],
            "SQL": ["SQLZoo", "Mode Analytics", "LeetCode SQL"],
            "Machine Learning": ["Andrew Ng ML Course", "Kaggle Learn", "Fast.ai"],
            
            # Business
            "Project Management": ["PMP Certification", "Agile Training", "Project Simulations"],
            "Leadership": ["Leadership Courses", "Management Training", "Team Building"],
            
            # Default
            "default": ["Online Courses", "Practical Training", "Industry Certification"]
        }
        
        # Create week-by-week plan
        roadmap = {}
        for i in range(4):
            skill_idx = i % len(skills_to_learn)
            skill = skills_to_learn[skill_idx]
            
            resources = resources_map.get(skill, resources_map["default"])
            
            if i == 0:
                topic = f"{skill} Fundamentals"
            elif i == 1:
                topic = f"{skill} Practice"
            elif i == 2:
                topic = f"Advanced {skill}"
            else:
                topic = "Integration & Review"
            
            roadmap[f"Week {i+1}"] = {
                "topic": topic if i < len(skills_to_learn) else f"Review & Practice",
                "resources": resources[:3] if isinstance(resources, list) else resources
            }
        
        return roadmap

    def chat_with_context(self, user_id: str, message: str, resume_context: Optional[Dict] = None, chat_history: List[Dict] = None) -> str:
        """Smart context-aware career counseling with conversation memory"""
        import random
        import hashlib
        
        # Get user context from memory or resume
        context = self.user_data.get(user_id, {})
        if resume_context and not context:
            context = {
                "target_role": resume_context.get("target_role", ""),
                "sector": self._detect_sector(resume_context.get("resume_content", ""), resume_context.get("target_role", ""))
            }
            self.user_data[user_id] = context
        
        target_role = context.get("target_role", "your desired career")
        sector = context.get("sector", "general")
        skills = context.get("skills_have", [])
        skills_need = context.get("skills_need", [])
        
        message_lower = message.lower().strip()
        
        # Analyze conversation history for context
        recent_topics = []
        user_name = None
        if chat_history:
            for msg in chat_history[-6:]:  # Last 6 messages for context
                content = msg.get("content", "").lower()
                if "resume" in content or "cv" in content:
                    recent_topics.append("resume")
                if "interview" in content:
                    recent_topics.append("interview")
                if "skill" in content or "learn" in content:
                    recent_topics.append("skills")
                if "salary" in content or "negotiate" in content:
                    recent_topics.append("salary")
                if "job" in content or "apply" in content:
                    recent_topics.append("job_search")
        
        # Generate varied responses based on message hash for consistency
        msg_hash = int(hashlib.md5(message.encode()).hexdigest()[:8], 16)
        variation = msg_hash % 3
        
        # Friendly greetings with memory
        if any(word in message_lower for word in ["hello", "hi", "hey", "good morning", "good evening"]):
            greetings = [
                f"Hey there! 👋 Great to see you! I'm here to help with your journey toward {target_role}. What's on your mind today?",
                f"Hello! Ready to work on your career goals? I remember you're interested in {target_role}. How can I help you today?",
                f"Hi! 🌟 Good to have you back! Let's continue working on your {target_role} career path. What would you like to discuss?"
            ]
            if resume_context:
                greetings[0] += " I see you've uploaded your resume, so I have good context about your background!"
            return greetings[variation]
        
        # Thank you responses
        if any(word in message_lower for word in ["thank", "thanks", "helpful", "great"]):
            thanks_responses = [
                f"You're welcome! 😊 I'm glad I could help. Feel free to ask me anything else about your {target_role} journey!",
                f"Happy to help! Remember, consistent effort is key. What else would you like to explore?",
                f"Anytime! Your dedication to career growth is inspiring. Let me know if you have more questions!"
            ]
            return thanks_responses[variation]
        
        # ========== RESUME CONTENT READING ==========
        resume_text = context.get("resume_text", "")
        
        # Questions about resume content
        if any(word in message_lower for word in ["my name", "what is my name", "who am i", "my resume"]):
            if resume_text:
                # Try to extract name from resume (usually at the top)
                lines = resume_text.strip().split('\n')
                # Name is usually in the first few non-empty lines
                potential_name = None
                for line in lines[:5]:
                    line = line.strip()
                    if line and len(line) < 50 and not any(char.isdigit() for char in line[:10]):
                        # Likely a name - short, no numbers at start
                        if '@' not in line and 'http' not in line.lower():
                            potential_name = line
                            break
                
                if potential_name:
                    return f"Based on your resume, your name is **{potential_name}**. Is there anything specific about your resume you'd like to discuss?"
                else:
                    return f"I have your resume loaded, but I couldn't clearly identify your name. The resume starts with:\n\n'{lines[0][:100]}...'\n\nWould you like me to help with something specific about your resume?"
            else:
                return "I don't have your resume loaded yet. Please upload your resume first so I can provide personalized advice!"
        
        # What's in my resume / Show my resume
        if any(phrase in message_lower for phrase in ["show my resume", "what's in my resume", "my resume content", "resume summary", "summarize my resume"]):
            if resume_text:
                # Provide a summary
                word_count = len(resume_text.split())
                lines = [l.strip() for l in resume_text.split('\n') if l.strip()]
                
                # Extract sections
                sections = []
                for word in ["experience", "education", "skills", "projects", "certifications", "summary"]:
                    if word in resume_text.lower():
                        sections.append(word.title())
                
                summary = f"📄 **Your Resume Summary:**\n\n"
                summary += f"• **Length**: ~{word_count} words\n"
                summary += f"• **Target Role**: {target_role}\n"
                if sections:
                    summary += f"• **Sections Found**: {', '.join(sections)}\n"
                if skills:
                    summary += f"• **Skills Identified**: {', '.join(skills[:5])}\n"
                summary += f"\n**First lines of your resume:**\n'{lines[0]}'\n'{lines[1] if len(lines) > 1 else ''}'\n\n"
                summary += "What would you like to discuss about your resume?"
                return summary
            else:
                return "I don't have your resume loaded yet. Please upload your resume first!"
        
        # Questions about experience
        if any(phrase in message_lower for phrase in ["my experience", "work experience", "past jobs", "previous work", "where did i work"]):
            if resume_text:
                # Try to extract experience section
                resume_lower = resume_text.lower()
                exp_start = -1
                for keyword in ["experience", "work history", "employment"]:
                    if keyword in resume_lower:
                        exp_start = resume_lower.find(keyword)
                        break
                
                if exp_start != -1:
                    # Extract some text after the experience keyword
                    exp_section = resume_text[exp_start:exp_start+500]
                    return f"📋 **From your resume - Experience section:**\n\n{exp_section[:400]}...\n\nWould you like tips on improving this section for {target_role}?"
                else:
                    return f"I couldn't find a clear 'Experience' section in your resume, but I have your full resume loaded. Would you like tips on adding work experience for {target_role}?"
            else:
                return "I don't have your resume loaded yet. Please upload your resume first!"
        
        # Questions about education
        if any(phrase in message_lower for phrase in ["my education", "my degree", "my school", "my university", "my college", "where did i study"]):
            if resume_text:
                resume_lower = resume_text.lower()
                edu_start = -1
                for keyword in ["education", "academic", "degree", "university", "college"]:
                    if keyword in resume_lower:
                        edu_start = resume_lower.find(keyword)
                        break
                
                if edu_start != -1:
                    edu_section = resume_text[edu_start:edu_start+400]
                    return f"🎓 **From your resume - Education section:**\n\n{edu_section[:350]}...\n\nWould you like tips on how to present your education for {target_role}?"
                else:
                    return f"I couldn't find a clear 'Education' section in your resume. Would you like guidance on what education to include for {target_role}?"
            else:
                return "I don't have your resume loaded yet. Please upload your resume first!"
        
        # Questions about skills from resume
        if any(phrase in message_lower for phrase in ["my skills", "what skills do i have", "skills from resume", "skills in my resume"]):
            if skills:
                return f"🔧 **Skills identified from your resume:**\n\n{', '.join(skills)}\n\n**Skills you should develop for {target_role}:**\n{', '.join(skills_need) if skills_need else 'Upload your resume for personalized recommendations!'}\n\nWould you like a roadmap to develop these skills?"
            elif resume_text:
                return f"I have your resume but haven't extracted detailed skills yet. Based on the content, you're targeting {target_role}. Would you like me to analyze your skills in more detail?"
            else:
                return "I don't have your resume loaded yet. Please upload your resume first!"
        
        # ========== ROADMAP MODIFICATION COMMANDS ==========
        current_roadmap = context.get("roadmap", {})
        
        # Show current roadmap
        if any(phrase in message_lower for phrase in ["show roadmap", "my roadmap", "current roadmap", "see roadmap", "view roadmap"]):
            if current_roadmap:
                roadmap_text = f"📍 **Your Current Learning Roadmap for {target_role}:**\n\n"
                for week, details in current_roadmap.items():
                    topic = details.get("topic", week)
                    resources = details.get("resources", [])
                    roadmap_text += f"**{week}:** {topic}\n"
                    roadmap_text += f"   📚 Resources: {', '.join(resources[:2])}\n\n"
                roadmap_text += "Would you like to modify any week? Just tell me what you'd like to change!"
                return roadmap_text
            else:
                return f"You don't have a roadmap yet! Upload your resume first, and I'll create a personalized learning path for {target_role}. Or tell me what skills you want to learn!"
        
        # Modify/change roadmap
        if any(phrase in message_lower for phrase in ["change roadmap", "modify roadmap", "update roadmap", "different roadmap", "new roadmap"]):
            return f"I'd be happy to modify your roadmap! 🔄 Here are options:\n\n1. **Add a topic** - Tell me: 'Add [skill] to my roadmap'\n2. **Remove a topic** - Tell me: 'Remove [skill] from my roadmap'\n3. **Focus on specific skill** - Tell me: 'Focus my roadmap on [skill]'\n4. **Extend duration** - Tell me: 'Make my roadmap 6 weeks'\n5. **Regenerate completely** - Tell me: 'Create a new roadmap for [goal]'\n\nWhat would you like to do?"
        
        # Add skill to roadmap
        if "add" in message_lower and "roadmap" in message_lower:
            # Extract the skill to add
            add_phrases = ["add", "include", "put"]
            skill_to_add = None
            for phrase in add_phrases:
                if phrase in message_lower:
                    parts = message_lower.split(phrase)
                    if len(parts) > 1:
                        remaining = parts[1].replace("to my roadmap", "").replace("to roadmap", "").replace("in my roadmap", "").strip()
                        skill_to_add = remaining.split()[0].capitalize() if remaining else None
            
            if skill_to_add and current_roadmap:
                # Add new week with this skill
                week_num = len(current_roadmap) + 1
                new_week = {
                    "topic": f"{skill_to_add} Fundamentals",
                    "resources": ["Online courses", "Documentation", "Practice projects"]
                }
                current_roadmap[f"Week {week_num}"] = new_week
                self.user_data[user_id]["roadmap"] = current_roadmap
                return f"✅ Done! I've added **{skill_to_add}** to your roadmap as Week {week_num}.\n\nYour roadmap now has {week_num} weeks. Want to see the updated roadmap? Just say 'show my roadmap'!"
            else:
                return f"I can add a skill to your roadmap! What skill would you like to add? For example: 'Add Python to my roadmap'"
        
        # Focus roadmap on specific skill
        if "focus" in message_lower and ("roadmap" in message_lower or "learning" in message_lower):
            # Extract focus skill
            focus_skill = None
            words = message_lower.replace("focus", "").replace("on", "").replace("my", "").replace("roadmap", "").replace("learning", "").strip().split()
            if words:
                focus_skill = words[0].capitalize()
            
            if focus_skill:
                # Regenerate roadmap focused on this skill
                new_roadmap = self.generate_roadmap([focus_skill], target_role)
                self.user_data[user_id]["roadmap"] = new_roadmap
                return f"🎯 Great choice! I've restructured your roadmap to focus on **{focus_skill}**.\n\nYour new 4-week learning path:\n\n" + "\n".join([f"**{k}:** {v['topic']}" for k, v in new_roadmap.items()]) + "\n\nThis intensive focus will help you master it faster! Say 'show my roadmap' for full details."
            else:
                return f"What skill would you like to focus on? Tell me: 'Focus my roadmap on [skill name]'"
        
        # Extend roadmap duration
        if ("extend" in message_lower or "longer" in message_lower or "more weeks" in message_lower) and "roadmap" in message_lower:
            if current_roadmap and skills_need:
                # Add more weeks
                current_weeks = len(current_roadmap)
                new_weeks = current_weeks + 2
                for i in range(current_weeks, new_weeks):
                    skill_idx = i % len(skills_need)
                    skill = skills_need[skill_idx]
                    current_roadmap[f"Week {i+1}"] = {
                        "topic": f"Advanced {skill}",
                        "resources": ["Advanced courses", "Real projects", "Mentorship"]
                    }
                self.user_data[user_id]["roadmap"] = current_roadmap
                return f"📅 Extended! Your roadmap now has **{new_weeks} weeks** instead of {current_weeks}.\n\nThe new weeks focus on advanced topics in your skill areas. Say 'show my roadmap' to see the full plan!"
            else:
                return f"I can extend your roadmap once you have one! Upload your resume first, or tell me what skills you want to learn."
        
        # Regenerate roadmap with new goal
        if "create" in message_lower and ("roadmap" in message_lower or "plan" in message_lower):
            # Extract new goal
            new_goal = message_lower.replace("create", "").replace("new", "").replace("roadmap", "").replace("plan", "").replace("for", "").replace("a", "").strip()
            if new_goal and len(new_goal) > 2:
                # Detect skills for new goal
                new_skills = self._get_missing_skills([], new_goal.title())
                new_roadmap = self.generate_roadmap(new_skills, new_goal.title())
                self.user_data[user_id]["roadmap"] = new_roadmap
                self.user_data[user_id]["roadmap_goal"] = new_goal.title()
                return f"🚀 Created a fresh roadmap for **{new_goal.title()}**!\n\n" + "\n".join([f"**{k}:** {v['topic']}" for k, v in new_roadmap.items()]) + f"\n\nThis plan targets the key skills needed for {new_goal.title()}. Let me know if you want to modify anything!"
            else:
                return f"I'll create a custom roadmap! What's your new career goal? Tell me: 'Create a roadmap for [role/goal]'"
        
        # Roadmap progress and tips
        if "roadmap" in message_lower and ("tip" in message_lower or "advice" in message_lower or "help" in message_lower):
            if current_roadmap:
                first_week = list(current_roadmap.values())[0]
                topic = first_week.get("topic", "your first topic")
                return f"💡 **Tips for your roadmap:**\n\n1. **Start with Week 1**: Focus on '{topic}' before moving on\n2. **Dedicate time**: Block 1-2 hours daily\n3. **Practice actively**: Don't just read - build things!\n4. **Track progress**: Check off completed topics\n5. **Ask questions**: Use this chat for guidance anytime\n\nWhich week are you currently on? I can give you specific advice!"
            else:
                return f"Let me create a roadmap for you first! Upload your resume, or tell me what skills you want to learn."
        
        # Follow-up detection - if discussing same topic
        if "more" in message_lower or "else" in message_lower or "another" in message_lower:
            if "resume" in recent_topics:
                tips = [
                    f"Here's another resume tip: Use action verbs like 'led', 'developed', 'achieved' to start your bullet points. They make your experience more impactful!",
                    f"Another thing to consider: Customize your resume summary for each application. A targeted summary shows you understand the role.",
                    f"Pro tip: Include a 'Key Achievements' section near the top. Recruiters often skim, so front-load your best accomplishments!"
                ]
                return tips[variation]
            elif "interview" in recent_topics:
                tips = [
                    f"Here's more interview advice: Practice the 'What's your weakness?' question. Choose a real weakness you're actively improving!",
                    f"Another interview tip: Send a thank-you email within 24 hours. Reference something specific you discussed - it shows you were engaged.",
                    f"Remember: Body language matters! Maintain eye contact, sit up straight, and give a firm handshake. Confidence is key!"
                ]
                return tips[variation]
        
        # Resume/CV discussions with context awareness
        if any(word in message_lower for word in ["resume", "cv", "ats"]):
            if "improve" in message_lower or "better" in message_lower or "tips" in message_lower:
                if sector in ["medical", "nursing", "physio"]:
                    responses = [
                        f"For your {target_role} resume, here are key improvements:\n\n• **Certifications first**: List your licenses and certifications prominently\n• **Clinical hours**: Include total clinical/patient care hours\n• **Specializations**: Highlight any specialized training or rotations\n• **Soft skills**: Don't forget patient communication and bedside manner",
                        f"Let's make your healthcare resume stand out! Focus on:\n\n1. Quantify patient interactions (e.g., 'Managed care for 20+ patients daily')\n2. List specific procedures you're trained in\n3. Include any quality or safety achievements\n4. Mention EHR systems you've used"
                    ]
                else:
                    responses = [
                        f"Let's improve your {target_role} resume! Here's what I suggest:\n\n• **Quantify everything**: Use numbers to show impact\n• **Keywords matter**: Mirror language from job postings\n• **Clean format**: Use simple fonts and clear sections\n• **Tailor it**: Customize for each application",
                        f"Great question! For {target_role}, your resume should:\n\n1. Start with a powerful summary (2-3 lines max)\n2. List achievements, not just duties\n3. Include relevant technical skills\n4. Keep it to 1-2 pages"
                    ]
                return responses[variation % len(responses)]
            else:
                base = f"I'd love to help with your resume! Based on your goal of becoming a {target_role}"
                if skills:
                    base += f", I see you already have skills in {', '.join(skills[:3])}. "
                base += " What specific aspect would you like to work on - format, content, or ATS optimization?"
                return base
        
        # Interview preparation with history context
        if any(word in message_lower for word in ["interview", "prepare", "question"]):
            if "tell me about yourself" in message_lower or "introduce" in message_lower:
                return f"Great question! For 'Tell me about yourself' in a {target_role} interview:\n\n**Use this formula:**\n1. Present: What you're doing now (1 sentence)\n2. Past: Relevant experience that led here (2 sentences)\n3. Future: Why you want this role (1 sentence)\n\n**Example structure:**\n'I'm currently [your situation]. Over the past [X years], I've [key achievements]. I'm excited about this opportunity because [connection to the role].'\n\nWant me to help you draft yours?"
            
            elif "weakness" in message_lower:
                return f"The 'weakness' question is tricky but manageable! Here's my advice:\n\n**DO:**\n• Choose a real but manageable weakness\n• Show you're actively improving\n• Never say 'perfectionism' or 'working too hard'\n\n**Example for {target_role}:**\n'I used to struggle with [specific skill]. I've addressed this by [specific action]. Now I [improvement shown].'\n\nWould you like to brainstorm a weakness together?"
            
            else:
                interview_tips = [
                    f"For your {target_role} interview, let me share some key strategies:\n\n📌 **Research**: Know the company's recent news and values\n📌 **STAR Method**: Structure answers as Situation, Task, Action, Result\n📌 **Questions**: Prepare 3-5 thoughtful questions to ask them\n📌 **Practice**: Do mock interviews out loud\n\nWhich area would you like to dive deeper into?",
                    f"Interview prep for {target_role}! Here's your game plan:\n\n1. **Know your story** - Why this role? Why now?\n2. **Prepare examples** - 5-6 stories that showcase your skills\n3. **Technical prep** - Review any role-specific knowledge\n4. **Logistics** - Plan your route, outfit, and materials\n\nWhat's your biggest interview concern right now?"
                ]
                return interview_tips[variation % len(interview_tips)]
        
        # Skills and learning
        if any(word in message_lower for word in ["skill", "learn", "course", "improve", "study"]):
            if skills_need:
                skill_focus = skills_need[0] if skills_need else "industry-relevant skills"
                responses = [
                    f"Based on your profile, I'd recommend focusing on **{skill_focus}** first. Here's why:\n\n• It's in high demand for {target_role}\n• It complements your existing skills\n• There are great free resources available\n\nWould you like specific learning resources for {skill_focus}?",
                    f"For your {target_role} goals, let's prioritize skill building:\n\n**Skills to develop:** {', '.join(skills_need[:3])}\n\nI suggest starting with {skill_focus} - it'll have the biggest impact on your job prospects. Want me to create a learning roadmap?"
                ]
                return responses[variation % len(responses)]
            else:
                return f"Let's work on your skill development! For {target_role}, the key areas to focus on are:\n\n• Technical skills specific to the role\n• Soft skills like communication and leadership\n• Industry certifications\n\nHave you uploaded your resume? That would help me give more personalized recommendations!"
        
        # Career path and transitions
        if any(word in message_lower for word in ["career", "path", "switch", "transition", "change", "growth"]):
            responses = [
                f"Career growth toward {target_role} is an exciting journey! Let me share a strategic approach:\n\n**Short-term (0-3 months):**\n• Fill skill gaps through courses\n• Update your resume and LinkedIn\n• Start networking in the field\n\n**Medium-term (3-6 months):**\n• Apply strategically to target roles\n• Build a portfolio of relevant work\n• Seek mentorship\n\nWhat stage are you in right now?",
                f"I love helping with career transitions! For your move toward {target_role}:\n\n🎯 **Assess**: What transferable skills do you already have?\n📚 **Learn**: What gaps need filling?\n🤝 **Connect**: Who can help you get there?\n🚀 **Act**: What's your first concrete step?\n\nShall we work through any of these together?"
            ]
            return responses[variation % len(responses)]
        
        # Salary and negotiation
        if any(word in message_lower for word in ["salary", "negotiate", "offer", "compensation", "pay"]):
            responses = [
                f"Salary negotiation is so important! Here's my advice for {target_role}:\n\n💰 **Research**: Check Glassdoor, LinkedIn Salary, Levels.fyi for market rates\n📊 **Know your worth**: Factor in experience, skills, and location\n🗣️ **Practice**: Rehearse your ask out loud\n⏰ **Timing**: Negotiate after receiving an offer, not before\n\n**Key phrase to use:**\n'Based on my research and experience, I was expecting something in the range of [X-Y].'\n\nWant to discuss your specific situation?",
                f"Let's talk compensation! For {target_role} roles, here's what matters:\n\n1. **Total package**: Consider benefits, bonuses, equity, not just base\n2. **Market data**: Always know the going rate before negotiating\n3. **Confidence**: They made an offer because they want YOU\n4. **Flexibility**: Be willing to negotiate other terms too\n\nDo you have an offer to discuss?"
            ]
            return responses[variation % len(responses)]
        
        # Job search strategies
        if any(word in message_lower for word in ["job", "apply", "search", "find", "hunting", "application"]):
            responses = [
                f"Job searching for {target_role} positions? Here's a smart strategy:\n\n**Quality over quantity:**\n• Customize each application\n• Research companies before applying\n• Network your way in when possible\n\n**Where to look:**\n• LinkedIn (set job alerts!)\n• Company career pages\n• Industry-specific job boards\n• Referrals (80% of jobs!)\n\nHow's your current search going?",
                f"Let me help optimize your job search for {target_role}!\n\n📝 **Track applications** in a spreadsheet\n🎯 **Focus on fit** - quality > quantity\n📧 **Follow up** after 1 week if no response\n🤝 **Network actively** - most jobs come through connections\n\nWhat part of the job search is most challenging for you?"
            ]
            return responses[variation % len(responses)]
        
        # Networking
        if any(word in message_lower for word in ["network", "connect", "linkedin", "people"]):
            return f"Networking is crucial for {target_role}! Here's how to do it authentically:\n\n**Online:**\n• Optimize your LinkedIn profile\n• Engage with industry content\n• Send personalized connection requests\n\n**Offline:**\n• Attend industry events and meetups\n• Join professional associations\n• Request informational interviews\n\n**Key tip:** Give before you ask. Share value, then people want to help you!\n\nWould you like specific networking scripts or templates?"
        
        # Contextual follow-up based on history
        if chat_history and len(chat_history) > 2:
            # Reference previous conversation
            last_assistant_msg = None
            for msg in reversed(chat_history):
                if msg.get("role") == "assistant":
                    last_assistant_msg = msg.get("content", "")
                    break
            
            if last_assistant_msg and len(message_lower) < 50:
                # Short follow-up message, continue the thread
                if "yes" in message_lower or "sure" in message_lower or "please" in message_lower:
                    if "resume" in last_assistant_msg.lower():
                        return f"Perfect! Let's work on your resume. First, what's your current biggest challenge - is it the format, content, or getting past ATS systems?"
                    elif "interview" in last_assistant_msg.lower():
                        return f"Great! Let's prepare you for interviews. Would you like to practice some common questions, or work on your 'tell me about yourself' story?"
                    elif "skill" in last_assistant_msg.lower() or "learn" in last_assistant_msg.lower():
                        return f"Awesome! I'll help you build a learning plan. What's your preferred learning style - video courses, hands-on projects, or reading documentation?"
        
        # Default friendly response
        defaults = [
            f"I'm here to help with your {target_role} career journey! 🌟 I can assist with:\n\n• Resume/CV optimization\n• Interview preparation\n• Skill development plans\n• Job search strategies\n• Salary negotiation\n• Career transitions\n\nWhat would you like to explore?",
            f"Great question! While I think about the best way to help you with that, here are the main areas I can assist with for your {target_role} path:\n\n1. 📄 Resume & ATS\n2. 🎤 Interview Prep\n3. 📚 Skill Building\n4. 💼 Job Search\n5. 💰 Salary Tips\n\nWhich area interests you most?",
            f"I'd love to help you succeed as a {target_role}! Could you tell me a bit more about what you're working on? For example:\n\n• Are you updating your resume?\n• Preparing for interviews?\n• Learning new skills?\n• Exploring career options?\n\nThe more context you share, the better I can assist!"
        ]
        return defaults[variation]

