export interface User {
  id: string;
  name: string;
  email: string;
  role: 'student' | 'professional' | 'expert' | 'admin';
  expertise?: string[];
  affiliation?: string;
  verified: boolean;
  joinedDate: string;
  avatar?: string;
  bio?: string;
}

export interface ForumPost {
  id: string;
  title: string;
  content: string;
  author: User;
  category: ForumCategory;
  tags: string[];
  createdAt: string;
  updatedAt: string;
  likes: number;
  replies: number;
  views: number;
}

export interface Reply {
  id: string;
  postId: string;
  content: string;
  author: User;
  createdAt: string;
  likes: number;
}

export type ForumCategory =
  | 'General Discussion'
  | 'Career Guidance'
  | 'Technical Questions'
  | 'Industry Insights'
  | 'Academia'
  | 'Startups'
  | 'Job Opportunities'
  | 'Scholarships';

export interface UniversityProgram {
  id: string;
  universityName: string;
  programName: string;
  degree: 'BS' | 'MS' | 'PhD' | 'Diploma';
  discipline: string;
  location: string;
  accreditation: string[];
  duration: string;
  overview: string;
  pros: string[];
  cons: string[];
  reviews: ProgramReview[];
  averageRating: number;
  employabilityScore?: number;
  researchOpportunities?: boolean;
}

export interface ProgramReview {
  id: string;
  programId: string;
  author: User;
  rating: number;
  content: string;
  graduationYear?: string;
  createdAt: string;
  helpful: number;
}

export interface CareerPath {
  id: string;
  title: string;
  discipline: string;
  overview: string;
  skills: string[];
  industries: string[];
  salaryRange: string;
  growthOutlook: string;
  educationRequired: string;
  experienceStories: ExperienceStory[];
}

export interface ExperienceStory {
  id: string;
  author: User;
  careerPathId: string;
  title: string;
  content: string;
  currentPosition: string;
  yearsOfExperience: number;
  createdAt: string;
}

export interface Job {
  id: string;
  title: string;
  company: string;
  location: string;
  type: 'Full-time' | 'Part-time' | 'Contract' | 'Internship';
  discipline: string;
  experienceLevel: 'Entry' | 'Mid' | 'Senior' | 'Lead';
  description: string;
  requirements: string[];
  salary?: string;
  postedDate: string;
  applicationUrl: string;
}

export interface Scholarship {
  id: string;
  name: string;
  provider: string;
  country: string;
  level: 'Undergraduate' | 'Graduate' | 'Doctoral' | 'Postdoctoral';
  disciplines: string[];
  amount: string;
  deadline: string;
  description: string;
  eligibility: string[];
  applicationUrl: string;
  funded: 'Fully Funded' | 'Partially Funded';
}

export interface IndustryInsight {
  id: string;
  title: string;
  industry: string;
  content: string;
  author: User;
  discipline: string;
  topics: string[];
  createdAt: string;
  views: number;
  helpful: number;
}

export interface SubjectConnection {
  id: string;
  subject: string;
  relatedSubjects: string[];
  applications: string[];
  careerPaths: string[];
  description: string;
}

export interface StartupResource {
  id: string;
  title: string;
  category: 'Funding' | 'Incubator' | 'Accelerator' | 'Mentorship' | 'Legal' | 'Technical' | 'Guide';
  description: string;
  provider: string;
  link?: string;
  eligibility?: string[];
  location?: string;
  createdAt: string;
}
