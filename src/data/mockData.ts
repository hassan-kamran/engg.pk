import {
  User,
  ForumPost,
  UniversityProgram,
  CareerPath,
  Job,
  Scholarship,
  IndustryInsight,
  SubjectConnection,
  StartupResource
} from '../types';

// Mock Users
export const mockUsers: User[] = [
  {
    id: '1',
    name: 'Dr. Ahmed Khan',
    email: 'ahmed.khan@example.com',
    role: 'expert',
    expertise: ['Power Systems', 'Control Systems', 'Renewable Energy'],
    affiliation: 'NUST Islamabad',
    verified: true,
    joinedDate: '2024-01-15',
    bio: 'Professor of Electrical Engineering with 15 years of experience in power systems and renewable energy.'
  },
  {
    id: '2',
    name: 'Fatima Malik',
    email: 'fatima.malik@example.com',
    role: 'professional',
    expertise: ['Software Engineering', 'Cloud Computing'],
    affiliation: 'Tech Solutions Pvt Ltd',
    verified: true,
    joinedDate: '2024-02-20',
    bio: 'Senior Software Engineer working on cloud infrastructure and distributed systems.'
  }
];

// Mock Forum Posts
export const mockForumPosts: ForumPost[] = [
  {
    id: '1',
    title: 'How to maintain control systems in gas-fired power plants?',
    content: 'I recently joined a power plant as a maintenance engineer. I would like to understand the best practices for maintaining DCS and SCADA systems in gas-fired power plants. What are the common challenges and how to address them?',
    author: mockUsers[1],
    category: 'Technical Questions',
    tags: ['Power Plant', 'Control Systems', 'Maintenance'],
    createdAt: '2024-11-01T10:00:00Z',
    updatedAt: '2024-11-01T10:00:00Z',
    likes: 15,
    replies: 8,
    views: 234
  },
  {
    id: '2',
    title: 'Career paths in Pakistan for Mechanical Engineers',
    content: 'I am about to graduate with a BS in Mechanical Engineering. What are the best career opportunities available in Pakistan? Should I focus on industry or consider further studies?',
    author: mockUsers[0],
    category: 'Career Guidance',
    tags: ['Mechanical Engineering', 'Career', 'Pakistan'],
    createdAt: '2024-11-05T14:30:00Z',
    updatedAt: '2024-11-05T14:30:00Z',
    likes: 42,
    replies: 23,
    views: 567
  },
  {
    id: '3',
    title: 'Starting a tech startup in Pakistan - Challenges and Opportunities',
    content: 'Has anyone here started a tech startup in Pakistan? What were the main challenges you faced and how did you overcome them? Looking for advice on funding, team building, and market validation.',
    author: mockUsers[1],
    category: 'Startups',
    tags: ['Startups', 'Entrepreneurship', 'Technology'],
    createdAt: '2024-11-06T09:00:00Z',
    updatedAt: '2024-11-06T09:00:00Z',
    likes: 38,
    replies: 17,
    views: 412
  }
];

// Mock University Programs
export const mockUniversityPrograms: UniversityProgram[] = [
  {
    id: '1',
    universityName: 'NUST (National University of Sciences and Technology)',
    programName: 'Electrical Engineering',
    degree: 'BS',
    discipline: 'Electrical Engineering',
    location: 'Islamabad',
    accreditation: ['PEC', 'HEC'],
    duration: '4 years',
    overview: 'Comprehensive program covering power systems, electronics, control systems, and telecommunications.',
    pros: [
      'Strong faculty with industry experience',
      'Well-equipped labs and modern facilities',
      'Good placement record in top companies',
      'Research opportunities available',
      'Strong alumni network'
    ],
    cons: [
      'Highly competitive admission',
      'Intense workload',
      'Limited flexibility in course selection',
      'High fee structure compared to public universities'
    ],
    reviews: [],
    averageRating: 4.5,
    employabilityScore: 85,
    researchOpportunities: true
  },
  {
    id: '2',
    universityName: 'UET (University of Engineering and Technology)',
    programName: 'Mechanical Engineering',
    degree: 'BS',
    discipline: 'Mechanical Engineering',
    location: 'Lahore',
    accreditation: ['PEC', 'HEC'],
    duration: '4 years',
    overview: 'Traditional mechanical engineering program with focus on thermal systems, manufacturing, and design.',
    pros: [
      'Oldest engineering university in Pakistan',
      'Strong industry connections',
      'Affordable fee structure',
      'Excellent lab facilities',
      'High prestige and recognition'
    ],
    cons: [
      'Traditional teaching methods',
      'Large class sizes',
      'Limited exposure to modern software tools',
      'Bureaucratic processes'
    ],
    reviews: [],
    averageRating: 4.2,
    employabilityScore: 78,
    researchOpportunities: true
  },
  {
    id: '3',
    universityName: 'GIKI (Ghulam Ishaq Khan Institute)',
    programName: 'Computer Systems Engineering',
    degree: 'BS',
    discipline: 'Computer Engineering',
    location: 'Topi, KPK',
    accreditation: ['PEC', 'HEC'],
    duration: '4 years',
    overview: 'Rigorous program combining hardware and software with emphasis on system-level thinking.',
    pros: [
      'Excellent academic rigor',
      'Beautiful campus with modern facilities',
      'Strong focus on practical skills',
      'Merit-based scholarships available',
      'Small class sizes'
    ],
    cons: [
      'Remote location',
      'Strict academic policies',
      'Limited social activities',
      'Challenging curriculum'
    ],
    reviews: [],
    averageRating: 4.6,
    employabilityScore: 88,
    researchOpportunities: true
  }
];

// Mock Career Paths
export const mockCareerPaths: CareerPath[] = [
  {
    id: '1',
    title: 'Power Plant Engineer',
    discipline: 'Electrical Engineering',
    overview: 'Power plant engineers operate, maintain, and optimize electrical power generation facilities including thermal, hydro, and renewable energy plants.',
    skills: ['Control Systems', 'Power Systems', 'SCADA', 'DCS', 'Preventive Maintenance', 'Safety Protocols'],
    industries: ['Energy', 'Utilities', 'Oil & Gas'],
    salaryRange: 'PKR 50,000 - 250,000/month',
    growthOutlook: 'Steady growth with increasing demand for renewable energy expertise',
    educationRequired: 'BS in Electrical Engineering, certifications in control systems preferred',
    experienceStories: []
  },
  {
    id: '2',
    title: 'Automation Engineer',
    discipline: 'Electrical/Mechatronics Engineering',
    overview: 'Design and implement automated systems for manufacturing, processing, and industrial operations.',
    skills: ['PLC Programming', 'Industrial Automation', 'Robotics', 'HMI Design', 'Process Control'],
    industries: ['Manufacturing', 'Automotive', 'Food Processing', 'Pharmaceuticals'],
    salaryRange: 'PKR 60,000 - 300,000/month',
    growthOutlook: 'High growth as industries adopt Industry 4.0 technologies',
    educationRequired: 'BS in Electrical/Mechatronics Engineering',
    experienceStories: []
  },
  {
    id: '3',
    title: 'Software Engineer',
    discipline: 'Computer Science/Software Engineering',
    overview: 'Develop software applications, systems, and solutions for various platforms and industries.',
    skills: ['Programming', 'Data Structures', 'Algorithms', 'Web Development', 'Mobile Development', 'Cloud Computing'],
    industries: ['Technology', 'Finance', 'E-commerce', 'Healthcare', 'Startups'],
    salaryRange: 'PKR 40,000 - 500,000/month',
    growthOutlook: 'Excellent growth with high demand locally and internationally',
    educationRequired: 'BS in Computer Science/Software Engineering or equivalent',
    experienceStories: []
  }
];

// Mock Jobs
export const mockJobs: Job[] = [
  {
    id: '1',
    title: 'Maintenance Engineer - Power Plant',
    company: 'Sahiwal Coal Power Plant',
    location: 'Sahiwal, Punjab',
    type: 'Full-time',
    discipline: 'Electrical Engineering',
    experienceLevel: 'Mid',
    description: 'Responsible for maintaining and troubleshooting control systems, switchgear, and electrical equipment in a 1320MW coal-fired power plant.',
    requirements: [
      'BS in Electrical Engineering',
      '3-5 years experience in power plant maintenance',
      'Knowledge of DCS, SCADA, and PLC systems',
      'Understanding of electrical safety standards'
    ],
    salary: 'PKR 120,000 - 180,000/month',
    postedDate: '2024-11-01',
    applicationUrl: '#'
  },
  {
    id: '2',
    title: 'Software Engineer - Full Stack',
    company: 'Systems Limited',
    location: 'Lahore, Punjab',
    type: 'Full-time',
    discipline: 'Software Engineering',
    experienceLevel: 'Entry',
    description: 'Join our development team to build modern web applications using React, Node.js, and cloud technologies.',
    requirements: [
      'BS in Computer Science or related field',
      'Proficiency in JavaScript/TypeScript',
      'Experience with React and Node.js',
      'Understanding of databases and APIs'
    ],
    salary: 'PKR 60,000 - 90,000/month',
    postedDate: '2024-11-05',
    applicationUrl: '#'
  },
  {
    id: '3',
    title: 'Manufacturing Engineer',
    company: 'Packages Limited',
    location: 'Kasur, Punjab',
    type: 'Full-time',
    discipline: 'Mechanical Engineering',
    experienceLevel: 'Entry',
    description: 'Work on process optimization, quality control, and production efficiency in our packaging manufacturing facility.',
    requirements: [
      'BS in Mechanical/Industrial Engineering',
      'Understanding of manufacturing processes',
      'Knowledge of quality management systems',
      'Fresh graduates encouraged to apply'
    ],
    salary: 'PKR 50,000 - 70,000/month',
    postedDate: '2024-11-07',
    applicationUrl: '#'
  }
];

// Mock Scholarships
export const mockScholarships: Scholarship[] = [
  {
    id: '1',
    name: 'HEC Indigenous PhD Fellowship',
    provider: 'Higher Education Commission Pakistan',
    country: 'Pakistan',
    level: 'Doctoral',
    disciplines: ['All Engineering Disciplines'],
    amount: 'PKR 25,000/month stipend + tuition',
    deadline: '2024-12-31',
    description: 'Fellowship program for Pakistani students to pursue PhD in Pakistani universities.',
    eligibility: [
      'Pakistani national',
      'MS/MPhil degree with minimum 3.0 CGPA',
      'Admission in HEC-recognized university',
      'Age limit: 35 years'
    ],
    applicationUrl: 'https://hec.gov.pk',
    funded: 'Fully Funded'
  },
  {
    id: '2',
    name: 'DAAD Master\'s Scholarships',
    provider: 'DAAD Germany',
    country: 'Germany',
    level: 'Graduate',
    disciplines: ['Engineering', 'Technology', 'Sciences'],
    amount: '€934/month + insurance + travel',
    deadline: '2024-10-31',
    description: 'Scholarships for international students to pursue Master\'s degrees in Germany.',
    eligibility: [
      'Bachelor\'s degree with good academic record',
      'At least 2 years work experience preferred',
      'IELTS/TOEFL or German language proficiency',
      'Strong motivation and career plan'
    ],
    applicationUrl: 'https://www.daad.de',
    funded: 'Fully Funded'
  },
  {
    id: '3',
    name: 'Chevening Scholarships',
    provider: 'UK Government',
    country: 'United Kingdom',
    level: 'Graduate',
    disciplines: ['All disciplines including Engineering'],
    amount: 'Full tuition + living allowance + airfare',
    deadline: '2024-11-07',
    description: 'UK government\'s global scholarship programme for future leaders.',
    eligibility: [
      'Pakistani national',
      'Undergraduate degree',
      'At least 2 years work experience',
      'Leadership potential',
      'Return to Pakistan for at least 2 years'
    ],
    applicationUrl: 'https://www.chevening.org',
    funded: 'Fully Funded'
  }
];

// Mock Industry Insights
export const mockIndustryInsights: IndustryInsight[] = [
  {
    id: '1',
    title: 'The Future of Power Generation in Pakistan',
    industry: 'Energy',
    content: 'Pakistan is transitioning towards renewable energy with targets of 30% renewable energy by 2030. This shift creates opportunities for engineers skilled in solar, wind, and hybrid systems. The control systems in modern power plants are becoming increasingly sophisticated, requiring engineers to understand both traditional power systems and modern automation technologies...',
    author: mockUsers[0],
    discipline: 'Electrical Engineering',
    topics: ['Renewable Energy', 'Power Systems', 'Control Systems'],
    createdAt: '2024-10-15',
    views: 1245,
    helpful: 89
  },
  {
    id: '2',
    title: 'Pakistan\'s Growing Tech Industry: Opportunities and Challenges',
    industry: 'Technology',
    content: 'Pakistan\'s IT industry has grown to $3.5 billion in exports, with a growth rate of 25% annually. However, there is a significant skill gap in areas like cloud computing, AI/ML, and cybersecurity. Engineers who upskill in these areas have excellent opportunities both locally and internationally...',
    author: mockUsers[1],
    discipline: 'Software Engineering',
    topics: ['Software Development', 'Cloud Computing', 'Career Growth'],
    createdAt: '2024-10-20',
    views: 2134,
    helpful: 156
  }
];

// Mock Subject Connections
export const mockSubjectConnections: SubjectConnection[] = [
  {
    id: '1',
    subject: 'Control Systems',
    relatedSubjects: ['Signals and Systems', 'Mathematics', 'Power Electronics', 'Digital Signal Processing'],
    applications: [
      'Power plant automation',
      'Industrial process control',
      'Robotics',
      'Automotive systems',
      'HVAC systems'
    ],
    careerPaths: ['Power Plant Engineer', 'Automation Engineer', 'Robotics Engineer', 'Process Control Engineer'],
    description: 'Control systems theory forms the foundation for automated systems across all industries. Understanding feedback, stability, and control design is crucial for modern engineering applications.'
  },
  {
    id: '2',
    subject: 'Data Structures and Algorithms',
    relatedSubjects: ['Programming Fundamentals', 'Discrete Mathematics', 'Database Systems', 'Operating Systems'],
    applications: [
      'Software development',
      'System design',
      'Database optimization',
      'AI and machine learning',
      'Network routing'
    ],
    careerPaths: ['Software Engineer', 'Data Engineer', 'Backend Developer', 'System Architect'],
    description: 'Core computer science subject essential for efficient problem-solving and software development. Critical for technical interviews and system design.'
  }
];

// Mock Startup Resources
export const mockStartupResources: StartupResource[] = [
  {
    id: '1',
    title: 'National Incubation Centers (NICs)',
    category: 'Incubator',
    description: 'Nationwide incubation centers providing workspace, mentorship, and funding opportunities for tech startups.',
    provider: 'Ignite - National Technology Fund',
    link: 'https://ignite.org.pk',
    eligibility: ['Tech-based startup idea', 'Team of 2-5 members', 'Pakistani nationals'],
    location: 'Islamabad, Lahore, Karachi, Peshawar, Quetta',
    createdAt: '2024-01-01'
  },
  {
    id: '2',
    title: 'Startup Pakistan Portal',
    category: 'Guide',
    description: 'Government portal for startup registration, licensing, and regulatory compliance.',
    provider: 'SECP Pakistan',
    link: 'https://startup.secp.gov.pk',
    eligibility: ['Any Pakistani entrepreneur'],
    location: 'Online',
    createdAt: '2024-01-01'
  },
  {
    id: '3',
    title: 'Pakistan Venture Capital Fund',
    category: 'Funding',
    description: 'Seed and early-stage funding for technology startups in Pakistan.',
    provider: 'PVCF',
    eligibility: ['Registered startup', 'Minimum viable product', 'Scalable business model'],
    location: 'Pakistan',
    createdAt: '2024-01-01'
  }
];
