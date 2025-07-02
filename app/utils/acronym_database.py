#!/usr/bin/env python3
"""
Comprehensive Acronym Database for DOCX Quality Control Checker
Professional acronym management system with extensive coverage
"""

import re
from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass

@dataclass
class AcronymDefinition:
    """Represents an acronym definition"""
    acronym: str
    full_name: str
    category: str
    description: Optional[str] = None
    is_common: bool = False

class AcronymDatabase:
    """
    Professional acronym database with comprehensive coverage
    Supports multiple categories and smart detection
    """
    
    def __init__(self):
        self.acronyms: Dict[str, AcronymDefinition] = {}
        self.categories: Dict[str, Set[str]] = {}
        self._build_database()
    
    def _build_database(self):
        """Build the comprehensive acronym database"""
        
        # Government and Regulatory Agencies
        government_acronyms = [
            ("FDA", "Food and Drug Administration", "Government", "US regulatory agency for food and drugs"),
            ("EPA", "Environmental Protection Agency", "Government", "US environmental regulatory agency"),
            ("WHO", "World Health Organization", "Government", "International health organization"),
            ("CDC", "Centers for Disease Control and Prevention", "Government", "US public health agency"),
            ("NIH", "National Institutes of Health", "Government", "US medical research agency"),
            ("NSF", "National Science Foundation", "Government", "US science funding agency"),
            ("OSHA", "Occupational Safety and Health Administration", "Government", "US workplace safety agency"),
            ("EMA", "European Medicines Agency", "Government", "European drug regulatory agency"),
            ("PMDA", "Pharmaceuticals and Medical Devices Agency", "Government", "Japanese drug regulatory agency"),
            ("NMPA", "National Medical Products Administration", "Government", "Chinese drug regulatory agency"),
            ("ISO", "International Organization for Standardization", "Government", "International standards organization"),
            ("ASTM", "American Society for Testing and Materials", "Government", "US standards organization"),
            ("ANSI", "American National Standards Institute", "Government", "US standards organization"),
            ("IEEE", "Institute of Electrical and Electronics Engineers", "Government", "Professional organization"),
            ("IEC", "International Electrotechnical Commission", "Government", "International standards organization"),
            ("ITU", "International Telecommunication Union", "Government", "UN telecommunications agency"),
            ("W3C", "World Wide Web Consortium", "Government", "Web standards organization"),
            ("OASIS", "Organization for the Advancement of Structured Information Standards", "Government", "Standards organization"),
        ]
        
        # Technology and Computing
        technology_acronyms = [
            ("API", "Application Programming Interface", "Technology", "Software interface for applications"),
            ("URL", "Uniform Resource Locator", "Technology", "Web address identifier"),
            ("HTTP", "Hypertext Transfer Protocol", "Technology", "Web communication protocol"),
            ("HTTPS", "Hypertext Transfer Protocol Secure", "Technology", "Secure web communication protocol"),
            ("PDF", "Portable Document Format", "Technology", "Document format"),
            ("XML", "Extensible Markup Language", "Technology", "Data markup language"),
            ("JSON", "JavaScript Object Notation", "Technology", "Data interchange format"),
            ("SQL", "Structured Query Language", "Technology", "Database query language"),
            ("CSS", "Cascading Style Sheets", "Technology", "Web styling language"),
            ("HTML", "Hypertext Markup Language", "Technology", "Web markup language"),
            ("GUI", "Graphical User Interface", "Technology", "Visual computer interface"),
            ("CLI", "Command Line Interface", "Technology", "Text-based computer interface"),
            ("IDE", "Integrated Development Environment", "Technology", "Software development tool"),
            ("SDK", "Software Development Kit", "Technology", "Development toolkit"),
            ("REST", "Representational State Transfer", "Technology", "Web service architecture"),
            ("SOAP", "Simple Object Access Protocol", "Technology", "Web service protocol"),
            ("CRUD", "Create, Read, Update, Delete", "Technology", "Database operations"),
            ("MVC", "Model-View-Controller", "Technology", "Software architecture pattern"),
            ("ORM", "Object-Relational Mapping", "Technology", "Database programming technique"),
            ("JWT", "JSON Web Token", "Technology", "Authentication token format"),
            ("OAuth", "Open Authorization", "Technology", "Authorization protocol"),
            ("SSL", "Secure Sockets Layer", "Technology", "Security protocol"),
            ("TLS", "Transport Layer Security", "Technology", "Security protocol"),
            ("SSH", "Secure Shell", "Technology", "Secure network protocol"),
            ("FTP", "File Transfer Protocol", "Technology", "File transfer protocol"),
            ("SMTP", "Simple Mail Transfer Protocol", "Technology", "Email protocol"),
            ("POP3", "Post Office Protocol 3", "Technology", "Email protocol"),
            ("IMAP", "Internet Message Access Protocol", "Technology", "Email protocol"),
            ("DNS", "Domain Name System", "Technology", "Internet naming system"),
            ("DHCP", "Dynamic Host Configuration Protocol", "Technology", "Network configuration protocol"),
            ("TCP", "Transmission Control Protocol", "Technology", "Network protocol"),
            ("UDP", "User Datagram Protocol", "Technology", "Network protocol"),
            ("IP", "Internet Protocol", "Technology", "Network protocol"),
            ("MAC", "Media Access Control", "Technology", "Network address"),
            ("LAN", "Local Area Network", "Technology", "Local computer network"),
            ("WAN", "Wide Area Network", "Technology", "Wide computer network"),
            ("VPN", "Virtual Private Network", "Technology", "Secure network connection"),
            ("WiFi", "Wireless Fidelity", "Technology", "Wireless networking"),
            ("USB", "Universal Serial Bus", "Technology", "Computer connection standard"),
            ("HDMI", "High-Definition Multimedia Interface", "Technology", "Digital video/audio interface"),
            ("VGA", "Video Graphics Array", "Technology", "Video display standard"),
            ("DVI", "Digital Visual Interface", "Technology", "Digital video interface"),
            ("SATA", "Serial Advanced Technology Attachment", "Technology", "Computer storage interface"),
            ("PCI", "Peripheral Component Interconnect", "Technology", "Computer bus standard"),
            ("AGP", "Accelerated Graphics Port", "Technology", "Graphics interface"),
            ("RAM", "Random Access Memory", "Technology", "Computer memory"),
            ("ROM", "Read-Only Memory", "Technology", "Computer memory"),
            ("CPU", "Central Processing Unit", "Technology", "Computer processor"),
            ("GPU", "Graphics Processing Unit", "Technology", "Graphics processor"),
            ("SSD", "Solid State Drive", "Technology", "Storage device"),
            ("HDD", "Hard Disk Drive", "Technology", "Storage device"),
            ("CD", "Compact Disc", "Technology", "Optical storage"),
            ("DVD", "Digital Versatile Disc", "Technology", "Optical storage"),
            ("BLU", "Blu-ray", "Technology", "Optical storage"),
        ]
        
        # Business and Corporate
        business_acronyms = [
            ("CEO", "Chief Executive Officer", "Business", "Top corporate executive"),
            ("CFO", "Chief Financial Officer", "Business", "Financial executive"),
            ("CTO", "Chief Technology Officer", "Business", "Technology executive"),
            ("COO", "Chief Operating Officer", "Business", "Operations executive"),
            ("CMO", "Chief Marketing Officer", "Business", "Marketing executive"),
            ("CLO", "Chief Legal Officer", "Business", "Legal executive"),
            ("CIO", "Chief Information Officer", "Business", "Information technology executive"),
            ("HR", "Human Resources", "Business", "Personnel management"),
            ("IT", "Information Technology", "Business", "Technology department"),
            ("QA", "Quality Assurance", "Business", "Quality control"),
            ("QC", "Quality Control", "Business", "Quality management"),
            ("R&D", "Research and Development", "Business", "Research department"),
            ("PR", "Public Relations", "Business", "Public communications"),
            ("VP", "Vice President", "Business", "Senior executive"),
            ("DIR", "Director", "Business", "Management position"),
            ("MGR", "Manager", "Business", "Management position"),
            ("SR", "Senior", "Business", "Senior level"),
            ("JR", "Junior", "Business", "Junior level"),
            ("ASSOC", "Associate", "Business", "Associate level"),
            ("ASST", "Assistant", "Business", "Assistant position"),
            ("ADMIN", "Administrator", "Business", "Administrative position"),
            ("EXEC", "Executive", "Business", "Executive position"),
            ("DEPT", "Department", "Business", "Organizational unit"),
            ("DIV", "Division", "Business", "Organizational unit"),
            ("CORP", "Corporation", "Business", "Business entity"),
            ("INC", "Incorporated", "Business", "Business entity"),
            ("LLC", "Limited Liability Company", "Business", "Business entity"),
            ("LTD", "Limited", "Business", "Business entity"),
            ("CO", "Company", "Business", "Business entity"),
            ("PTY", "Proprietary", "Business", "Business entity"),
            ("PLC", "Public Limited Company", "Business", "Business entity"),
            ("AG", "Aktiengesellschaft", "Business", "German corporation"),
            ("SA", "Société Anonyme", "Business", "French corporation"),
            ("NV", "Naamloze Vennootschap", "Business", "Dutch corporation"),
            ("BV", "Besloten Vennootschap", "Business", "Dutch corporation"),
            ("GMBH", "Gesellschaft mit beschränkter Haftung", "Business", "German limited company"),
            ("KG", "Kommanditgesellschaft", "Business", "German partnership"),
            ("OHG", "Offene Handelsgesellschaft", "Business", "German partnership"),
            ("UG", "Unternehmergesellschaft", "Business", "German company"),
            ("SE", "Societas Europaea", "Business", "European company"),
            ("AB", "Aktiebolag", "Business", "Swedish corporation"),
            ("OY", "Osakeyhtiö", "Business", "Finnish corporation"),
            ("AS", "Aksjeselskap", "Business", "Norwegian corporation"),
            ("APS", "Anpartsselskab", "Business", "Danish corporation"),
            ("A/S", "Aktieselskab", "Business", "Danish corporation"),
        ]
        
        # Medical and Clinical
        medical_acronyms = [
            ("DNA", "Deoxyribonucleic Acid", "Medical", "Genetic material"),
            ("RNA", "Ribonucleic Acid", "Medical", "Genetic material"),
            ("ATP", "Adenosine Triphosphate", "Medical", "Energy molecule"),
            ("ADP", "Adenosine Diphosphate", "Medical", "Energy molecule"),
            ("AMP", "Adenosine Monophosphate", "Medical", "Energy molecule"),
            ("NAD", "Nicotinamide Adenine Dinucleotide", "Medical", "Coenzyme"),
            ("NADH", "Nicotinamide Adenine Dinucleotide Hydrogen", "Medical", "Reduced coenzyme"),
            ("FAD", "Flavin Adenine Dinucleotide", "Medical", "Coenzyme"),
            ("FADH", "Flavin Adenine Dinucleotide Hydrogen", "Medical", "Reduced coenzyme"),
            ("COA", "Coenzyme A", "Medical", "Coenzyme"),
            ("ACP", "Acyl Carrier Protein", "Medical", "Protein"),
            ("UDP", "Uridine Diphosphate", "Medical", "Nucleotide"),
            ("CDP", "Cytidine Diphosphate", "Medical", "Nucleotide"),
            ("GDP", "Guanosine Diphosphate", "Medical", "Nucleotide"),
            ("GTP", "Guanosine Triphosphate", "Medical", "Nucleotide"),
            ("CTP", "Cytidine Triphosphate", "Medical", "Nucleotide"),
            ("UTP", "Uridine Triphosphate", "Medical", "Nucleotide"),
            ("TTP", "Thymidine Triphosphate", "Medical", "Nucleotide"),
            ("DTT", "Dithiothreitol", "Medical", "Chemical compound"),
            ("EDTA", "Ethylenediaminetetraacetic Acid", "Medical", "Chelating agent"),
            ("PBS", "Phosphate-Buffered Saline", "Medical", "Buffer solution"),
            ("TBS", "Tris-Buffered Saline", "Medical", "Buffer solution"),
            ("SDS", "Sodium Dodecyl Sulfate", "Medical", "Detergent"),
            ("PAGE", "Polyacrylamide Gel Electrophoresis", "Medical", "Laboratory technique"),
            ("PCR", "Polymerase Chain Reaction", "Medical", "DNA amplification technique"),
            ("RT", "Reverse Transcriptase", "Medical", "Enzyme"),
            ("QPCR", "Quantitative Polymerase Chain Reaction", "Medical", "DNA quantification technique"),
            ("RTPCR", "Reverse Transcription Polymerase Chain Reaction", "Medical", "RNA amplification technique"),
            ("ELISA", "Enzyme-Linked Immunosorbent Assay", "Medical", "Laboratory test"),
            ("WB", "Western Blot", "Medical", "Protein detection technique"),
            ("IP", "Immunoprecipitation", "Medical", "Protein isolation technique"),
            ("CHIP", "Chromatin Immunoprecipitation", "Medical", "DNA-protein interaction technique"),
            ("FISH", "Fluorescence In Situ Hybridization", "Medical", "Genetic technique"),
            ("ISH", "In Situ Hybridization", "Medical", "Genetic technique"),
            ("IHC", "Immunohistochemistry", "Medical", "Tissue staining technique"),
            ("IF", "Immunofluorescence", "Medical", "Fluorescent staining technique"),
            ("FC", "Flow Cytometry", "Medical", "Cell analysis technique"),
            ("FACS", "Fluorescence-Activated Cell Sorting", "Medical", "Cell sorting technique"),
            ("MACS", "Magnetic-Activated Cell Sorting", "Medical", "Cell sorting technique"),
            ("TALEN", "Transcription Activator-Like Effector Nuclease", "Medical", "Gene editing tool"),
            ("CRISPR", "Clustered Regularly Interspaced Short Palindromic Repeats", "Medical", "Gene editing system"),
            ("CAS", "CRISPR-Associated Protein", "Medical", "CRISPR protein"),
        ]
        
        # Measurement Units
        measurement_acronyms = [
            ("KG", "Kilogram", "Measurement", "Mass unit"),
            ("LB", "Pound", "Measurement", "Mass unit"),
            ("OZ", "Ounce", "Measurement", "Mass unit"),
            ("G", "Gram", "Measurement", "Mass unit"),
            ("MG", "Milligram", "Measurement", "Mass unit"),
            ("UG", "Microgram", "Measurement", "Mass unit"),
            ("NG", "Nanogram", "Measurement", "Mass unit"),
            ("PG", "Picogram", "Measurement", "Mass unit"),
            ("M", "Meter", "Measurement", "Length unit"),
            ("CM", "Centimeter", "Measurement", "Length unit"),
            ("MM", "Millimeter", "Measurement", "Length unit"),
            ("UM", "Micrometer", "Measurement", "Length unit"),
            ("NM", "Nanometer", "Measurement", "Length unit"),
            ("KM", "Kilometer", "Measurement", "Length unit"),
            ("MI", "Mile", "Measurement", "Length unit"),
            ("YD", "Yard", "Measurement", "Length unit"),
            ("FT", "Foot", "Measurement", "Length unit"),
            ("IN", "Inch", "Measurement", "Length unit"),
            ("L", "Liter", "Measurement", "Volume unit"),
            ("ML", "Milliliter", "Measurement", "Volume unit"),
            ("UL", "Microliter", "Measurement", "Volume unit"),
            ("NL", "Nanoliter", "Measurement", "Volume unit"),
            ("PL", "Picoliter", "Measurement", "Volume unit"),
            ("GAL", "Gallon", "Measurement", "Volume unit"),
            ("QT", "Quart", "Measurement", "Volume unit"),
            ("PT", "Pint", "Measurement", "Volume unit"),
            ("CUP", "Cup", "Measurement", "Volume unit"),
            ("TBSP", "Tablespoon", "Measurement", "Volume unit"),
            ("TSP", "Teaspoon", "Measurement", "Volume unit"),
            ("FL", "Fluid", "Measurement", "Volume modifier"),
            ("C", "Celsius", "Measurement", "Temperature unit"),
            ("F", "Fahrenheit", "Measurement", "Temperature unit"),
            ("K", "Kelvin", "Measurement", "Temperature unit"),
            ("R", "Rankine", "Measurement", "Temperature unit"),
            ("PA", "Pascal", "Measurement", "Pressure unit"),
            ("PSI", "Pounds per Square Inch", "Measurement", "Pressure unit"),
            ("BAR", "Bar", "Measurement", "Pressure unit"),
            ("ATM", "Atmosphere", "Measurement", "Pressure unit"),
            ("TORR", "Torr", "Measurement", "Pressure unit"),
            ("MMHG", "Millimeters of Mercury", "Measurement", "Pressure unit"),
            ("INHG", "Inches of Mercury", "Measurement", "Pressure unit"),
            ("MB", "Millibar", "Measurement", "Pressure unit"),
            ("HPA", "Hectopascal", "Measurement", "Pressure unit"),
            ("KPA", "Kilopascal", "Measurement", "Pressure unit"),
            ("MPA", "Megapascal", "Measurement", "Pressure unit"),
            ("GPA", "Gigapascal", "Measurement", "Pressure unit"),
            ("J", "Joule", "Measurement", "Energy unit"),
            ("KJ", "Kilojoule", "Measurement", "Energy unit"),
            ("MJ", "Megajoule", "Measurement", "Energy unit"),
            ("CAL", "Calorie", "Measurement", "Energy unit"),
            ("KCAL", "Kilocalorie", "Measurement", "Energy unit"),
            ("BTU", "British Thermal Unit", "Measurement", "Energy unit"),
            ("WH", "Watt-hour", "Measurement", "Energy unit"),
            ("KWH", "Kilowatt-hour", "Measurement", "Energy unit"),
            ("MWH", "Megawatt-hour", "Measurement", "Energy unit"),
            ("EV", "Electron Volt", "Measurement", "Energy unit"),
            ("KEV", "Kiloelectron Volt", "Measurement", "Energy unit"),
            ("MEV", "Megaelectron Volt", "Measurement", "Energy unit"),
            ("GEV", "Gigaelectron Volt", "Measurement", "Energy unit"),
            ("TEV", "Teraelectron Volt", "Measurement", "Energy unit"),
            ("PEV", "Petaelectron Volt", "Measurement", "Energy unit"),
            ("HZ", "Hertz", "Measurement", "Frequency unit"),
            ("KHZ", "Kilohertz", "Measurement", "Frequency unit"),
            ("MHZ", "Megahertz", "Measurement", "Frequency unit"),
            ("GHZ", "Gigahertz", "Measurement", "Frequency unit"),
            ("THZ", "Terahertz", "Measurement", "Frequency unit"),
            ("PHZ", "Petahertz", "Measurement", "Frequency unit"),
            ("BPS", "Bits per Second", "Measurement", "Data rate unit"),
            ("KBPS", "Kilobits per Second", "Measurement", "Data rate unit"),
            ("MBPS", "Megabits per Second", "Measurement", "Data rate unit"),
            ("GBPS", "Gigabits per Second", "Measurement", "Data rate unit"),
            ("TBPS", "Terabits per Second", "Measurement", "Data rate unit"),
            ("PBPS", "Petabits per Second", "Measurement", "Data rate unit"),
            ("B", "Byte", "Measurement", "Data unit"),
            ("KB", "Kilobyte", "Measurement", "Data unit"),
            ("MB", "Megabyte", "Measurement", "Data unit"),
            ("GB", "Gigabyte", "Measurement", "Data unit"),
            ("TB", "Terabyte", "Measurement", "Data unit"),
            ("PB", "Petabyte", "Measurement", "Data unit"),
            ("EB", "Exabyte", "Measurement", "Data unit"),
            ("ZB", "Zettabyte", "Measurement", "Data unit"),
            ("YB", "Yottabyte", "Measurement", "Data unit"),
            ("BIT", "Binary Digit", "Measurement", "Data unit"),
            ("BYTE", "Byte", "Measurement", "Data unit"),
            ("WORD", "Word", "Measurement", "Data unit"),
            ("DWORD", "Double Word", "Measurement", "Data unit"),
            ("QWORD", "Quad Word", "Measurement", "Data unit"),
            ("NIBBLE", "Nibble", "Measurement", "Data unit"),
            ("OCTET", "Octet", "Measurement", "Data unit"),
            ("CHAR", "Character", "Measurement", "Data unit"),
            ("STRING", "String", "Measurement", "Data unit"),
            ("ARRAY", "Array", "Measurement", "Data structure"),
            ("LIST", "List", "Measurement", "Data structure"),
            ("STACK", "Stack", "Measurement", "Data structure"),
            ("QUEUE", "Queue", "Measurement", "Data structure"),
            ("TREE", "Tree", "Measurement", "Data structure"),
            ("GRAPH", "Graph", "Measurement", "Data structure"),
            ("HEAP", "Heap", "Measurement", "Data structure"),
            ("HASH", "Hash", "Measurement", "Data structure"),
            ("MAP", "Map", "Measurement", "Data structure"),
            ("SET", "Set", "Measurement", "Data structure"),
            ("VECTOR", "Vector", "Measurement", "Data structure"),
            ("MATRIX", "Matrix", "Measurement", "Data structure"),
            ("TENSOR", "Tensor", "Measurement", "Data structure"),
            ("SCALAR", "Scalar", "Measurement", "Data structure"),
        ]
        
        # Time Units
        time_acronyms = [
            ("SEC", "Second", "Time", "Time unit"),
            ("MIN", "Minute", "Time", "Time unit"),
            ("HR", "Hour", "Time", "Time unit"),
            ("DAY", "Day", "Time", "Time unit"),
            ("WEEK", "Week", "Time", "Time unit"),
            ("MONTH", "Month", "Time", "Time unit"),
            ("YEAR", "Year", "Time", "Time unit"),
            ("DECADE", "Decade", "Time", "Time unit"),
            ("CENTURY", "Century", "Time", "Time unit"),
            ("MILLENNIUM", "Millennium", "Time", "Time unit"),
            ("MS", "Millisecond", "Time", "Time unit"),
            ("US", "Microsecond", "Time", "Time unit"),
            ("NS", "Nanosecond", "Time", "Time unit"),
            ("PS", "Picosecond", "Time", "Time unit"),
            ("FS", "Femtosecond", "Time", "Time unit"),
            ("AS", "Attosecond", "Time", "Time unit"),
            ("ZS", "Zeptosecond", "Time", "Time unit"),
            ("YS", "Yoctosecond", "Time", "Time unit"),
            ("AM", "Ante Meridiem", "Time", "Time period"),
            ("PM", "Post Meridiem", "Time", "Time period"),
            ("GMT", "Greenwich Mean Time", "Time", "Time zone"),
            ("UTC", "Coordinated Universal Time", "Time", "Time zone"),
            ("EST", "Eastern Standard Time", "Time", "Time zone"),
            ("CST", "Central Standard Time", "Time", "Time zone"),
            ("MST", "Mountain Standard Time", "Time", "Time zone"),
            ("PST", "Pacific Standard Time", "Time", "Time zone"),
            ("EDT", "Eastern Daylight Time", "Time", "Time zone"),
            ("CDT", "Central Daylight Time", "Time", "Time zone"),
            ("MDT", "Mountain Daylight Time", "Time", "Time zone"),
            ("PDT", "Pacific Daylight Time", "Time", "Time zone"),
            ("BST", "British Summer Time", "Time", "Time zone"),
            ("CET", "Central European Time", "Time", "Time zone"),
            ("CEST", "Central European Summer Time", "Time", "Time zone"),
            ("EET", "Eastern European Time", "Time", "Time zone"),
            ("EEST", "Eastern European Summer Time", "Time", "Time zone"),
            ("JST", "Japan Standard Time", "Time", "Time zone"),
            ("KST", "Korea Standard Time", "Time", "Time zone"),
            ("IST", "India Standard Time", "Time", "Time zone"),
            ("AEST", "Australian Eastern Standard Time", "Time", "Time zone"),
            ("AEDT", "Australian Eastern Daylight Time", "Time", "Time zone"),
            ("ACST", "Australian Central Standard Time", "Time", "Time zone"),
            ("ACDT", "Australian Central Daylight Time", "Time", "Time zone"),
            ("AWST", "Australian Western Standard Time", "Time", "Time zone"),
            ("AWDT", "Australian Western Daylight Time", "Time", "Time zone"),
            ("NZST", "New Zealand Standard Time", "Time", "Time zone"),
            ("NZDT", "New Zealand Daylight Time", "Time", "Time zone"),
            ("FJT", "Fiji Time", "Time", "Time zone"),
            ("FJST", "Fiji Summer Time", "Time", "Time zone"),
            ("CHST", "Chamorro Standard Time", "Time", "Time zone"),
            ("CHADT", "Chamorro Daylight Time", "Time", "Time zone"),
            ("WST", "Western Standard Time", "Time", "Time zone"),
            ("WDT", "Western Daylight Time", "Time", "Time zone"),
            ("SST", "Samoa Standard Time", "Time", "Time zone"),
            ("SDT", "Samoa Daylight Time", "Time", "Time zone"),
            ("HST", "Hawaii Standard Time", "Time", "Time zone"),
            ("HDT", "Hawaii Daylight Time", "Time", "Time zone"),
            ("AKST", "Alaska Standard Time", "Time", "Time zone"),
            ("AKDT", "Alaska Daylight Time", "Time", "Time zone"),
            ("HAST", "Hawaii-Aleutian Standard Time", "Time", "Time zone"),
            ("HADT", "Hawaii-Aleutian Daylight Time", "Time", "Time zone"),
        ]
        
        # File Formats and Extensions
        file_acronyms = [
            ("MP3", "MPEG Audio Layer III", "File Format", "Audio format"),
            ("MP4", "MPEG-4 Part 14", "File Format", "Video format"),
            ("AVI", "Audio Video Interleave", "File Format", "Video format"),
            ("MOV", "QuickTime Movie", "File Format", "Video format"),
            ("WMV", "Windows Media Video", "File Format", "Video format"),
            ("FLV", "Flash Video", "File Format", "Video format"),
            ("WEBM", "WebM", "File Format", "Video format"),
            ("OGG", "Ogg Vorbis", "File Format", "Audio format"),
            ("WAV", "Waveform Audio File Format", "File Format", "Audio format"),
            ("AAC", "Advanced Audio Coding", "File Format", "Audio format"),
            ("FLAC", "Free Lossless Audio Codec", "File Format", "Audio format"),
            ("ZIP", "ZIP Archive", "File Format", "Archive format"),
            ("RAR", "RAR Archive", "File Format", "Archive format"),
            ("TAR", "Tape Archive", "File Format", "Archive format"),
            ("GZ", "Gzip", "File Format", "Compression format"),
            ("BZ2", "Bzip2", "File Format", "Compression format"),
            ("7Z", "7-Zip", "File Format", "Archive format"),
            ("ISO", "ISO Image", "File Format", "Disk image format"),
            ("EXE", "Executable", "File Format", "Executable file"),
            ("MSI", "Microsoft Installer", "File Format", "Installation package"),
            ("DEB", "Debian Package", "File Format", "Linux package"),
            ("RPM", "Red Hat Package Manager", "File Format", "Linux package"),
            ("DMG", "Disk Image", "File Format", "Mac disk image"),
            ("PKG", "Package", "File Format", "Mac package"),
            ("APK", "Android Package", "File Format", "Android app package"),
            ("IPA", "iOS App Store Package", "File Format", "iOS app package"),
            ("JAR", "Java Archive", "File Format", "Java package"),
            ("WAR", "Web Application Archive", "File Format", "Java web package"),
            ("EAR", "Enterprise Archive", "File Format", "Java enterprise package"),
        ]
        
        # Programming Languages
        programming_acronyms = [
            ("JS", "JavaScript", "Programming", "Programming language"),
            ("PHP", "PHP: Hypertext Preprocessor", "Programming", "Programming language"),
            ("PY", "Python", "Programming", "Programming language"),
            ("JAVA", "Java", "Programming", "Programming language"),
            ("CPP", "C++", "Programming", "Programming language"),
            ("CS", "C#", "Programming", "Programming language"),
            ("VB", "Visual Basic", "Programming", "Programming language"),
            ("SWIFT", "Swift", "Programming", "Programming language"),
            ("KOTLIN", "Kotlin", "Programming", "Programming language"),
            ("RUST", "Rust", "Programming", "Programming language"),
            ("GO", "Go", "Programming", "Programming language"),
            ("RUBY", "Ruby", "Programming", "Programming language"),
            ("PERL", "Perl", "Programming", "Programming language"),
            ("SCALA", "Scala", "Programming", "Programming language"),
            ("HASKELL", "Haskell", "Programming", "Programming language"),
            ("ERLANG", "Erlang", "Programming", "Programming language"),
            ("ELIXIR", "Elixir", "Programming", "Programming language"),
            ("CLOJURE", "Clojure", "Programming", "Programming language"),
            ("LISP", "LISP", "Programming", "Programming language"),
            ("SCHEME", "Scheme", "Programming", "Programming language"),
            ("PROLOG", "Prolog", "Programming", "Programming language"),
            ("FORTH", "Forth", "Programming", "Programming language"),
            ("ADA", "Ada", "Programming", "Programming language"),
            ("COBOL", "COBOL", "Programming", "Programming language"),
            ("FORTRAN", "FORTRAN", "Programming", "Programming language"),
            ("PASCAL", "Pascal", "Programming", "Programming language"),
            ("BASIC", "BASIC", "Programming", "Programming language"),
            ("ALGOL", "ALGOL", "Programming", "Programming language"),
            ("PL", "Programming Language", "Programming", "Generic term"),
            ("SNOBOL", "SNOBOL", "Programming", "Programming language"),
            ("APL", "APL", "Programming", "Programming language"),
            ("J", "J", "Programming", "Programming language"),
            ("K", "K", "Programming", "Programming language"),
            ("Q", "Q", "Programming", "Programming language"),
            ("MATLAB", "MATLAB", "Programming", "Programming language"),
            ("OCTAVE", "GNU Octave", "Programming", "Programming language"),
            ("R", "R", "Programming", "Programming language"),
            ("SAS", "SAS", "Programming", "Statistical software"),
            ("SPSS", "Statistical Package for the Social Sciences", "Programming", "Statistical software"),
            ("STATA", "Stata", "Programming", "Statistical software"),
            ("MINITAB", "Minitab", "Programming", "Statistical software"),
            ("JMP", "JMP", "Programming", "Statistical software"),
            ("SYSTAT", "SYSTAT", "Programming", "Statistical software"),
            ("STATGRAPHICS", "Statgraphics", "Programming", "Statistical software"),
            ("NCSS", "NCSS", "Programming", "Statistical software"),
            ("PASS", "PASS", "Programming", "Statistical software"),
            ("NQUERY", "nQuery", "Programming", "Statistical software"),
            ("SAMPLEPOWER", "SamplePower", "Programming", "Statistical software"),
            ("GPOWER", "G*Power", "Programming", "Statistical software"),
            ("G*POWER", "G*Power", "Programming", "Statistical software"),
            ("POWER", "Power", "Programming", "Statistical term"),
            ("SAMPLE", "Sample", "Programming", "Statistical term"),
            ("SIZE", "Size", "Programming", "Statistical term"),
            ("ANALYSIS", "Analysis", "Programming", "Statistical term"),
            ("STATISTICAL", "Statistical", "Programming", "Statistical term"),
            ("ANALYSIS", "Analysis", "Programming", "Statistical term"),
            ("SYSTEM", "System", "Programming", "Statistical term"),
            ("STATISTICAL", "Statistical", "Programming", "Statistical term"),
            ("PACKAGE", "Package", "Programming", "Statistical term"),
            ("FOR", "For", "Programming", "Statistical term"),
            ("SOCIAL", "Social", "Programming", "Statistical term"),
            ("SCIENCES", "Sciences", "Programming", "Statistical term"),
        ]
        
        # Common Document Terms
        document_acronyms = [
            ("LIST", "List", "Document", "Document element"),
            ("TABLE", "Table", "Document", "Document element"),
            ("FIGURE", "Figure", "Document", "Document element"),
            ("SECTION", "Section", "Document", "Document element"),
            ("CHAPTER", "Chapter", "Document", "Document element"),
            ("PAGE", "Page", "Document", "Document element"),
            ("APPENDIX", "Appendix", "Document", "Document element"),
            ("REFERENCE", "Reference", "Document", "Document element"),
            ("BIBLIOGRAPHY", "Bibliography", "Document", "Document element"),
        ]
        
        # Technical Placeholders and Common Terms
        technical_acronyms = [
            ("XXX", "Placeholder", "Technical", "Generic placeholder"),
            ("IB", "Information Bulletin", "Technical", "Document type"),
            ("DS", "Data Sheet", "Technical", "Document type"),
            ("DRF", "Data Request Form", "Technical", "Document type"),
            ("FIH", "First in Human", "Technical", "Clinical trial phase"),
            ("GLP", "Good Laboratory Practice", "Technical", "Laboratory standard"),
            ("MTD", "Maximum Tolerated Dose", "Technical", "Clinical term"),
            ("PK", "Public Key", "Technical", "Cryptographic key"),
            ("TK", "Technical Knowledge", "Technical", "Technical knowledge base"),
            ("HNSTD", "High Network Security Technical Documentation", "Technical", "Network security documentation"),
        ]
        
        # Combine all acronym categories
        all_acronyms = (
            government_acronyms + technology_acronyms + business_acronyms + 
            medical_acronyms + measurement_acronyms + time_acronyms + 
            file_acronyms + programming_acronyms + document_acronyms + 
            technical_acronyms
        )
        
        # Build the database
        for acronym, full_name, category, description in all_acronyms:
            self.acronyms[acronym] = AcronymDefinition(
                acronym=acronym,
                full_name=full_name,
                category=category,
                description=description,
                is_common=True
            )
            
            if category not in self.categories:
                self.categories[category] = set()
            self.categories[category].add(acronym)
    
    def get_acronym(self, acronym: str) -> Optional[AcronymDefinition]:
        """Get acronym definition by acronym"""
        return self.acronyms.get(acronym.upper())
    
    def is_known_acronym(self, acronym: str) -> bool:
        """Check if acronym is in the database"""
        return acronym.upper() in self.acronyms
    
    def get_acronyms_by_category(self, category: str) -> List[AcronymDefinition]:
        """Get all acronyms in a specific category"""
        if category not in self.categories:
            return []
        return [self.acronyms[acronym] for acronym in self.categories[category]]
    
    def search_acronyms(self, query: str) -> List[AcronymDefinition]:
        """Search acronyms by name or description"""
        query = query.lower()
        results = []
        
        for acronym_def in self.acronyms.values():
            if (query in acronym_def.acronym.lower() or
                query in acronym_def.full_name.lower() or
                (acronym_def.description and query in acronym_def.description.lower())):
                results.append(acronym_def)
        
        return results
    
    def add_acronym(self, acronym: str, full_name: str, category: str = "Custom", 
                   description: Optional[str] = None, is_common: bool = False):
        """Add a new acronym to the database"""
        acronym_upper = acronym.upper()
        self.acronyms[acronym_upper] = AcronymDefinition(
            acronym=acronym_upper,
            full_name=full_name,
            category=category,
            description=description,
            is_common=is_common
        )
        
        if category not in self.categories:
            self.categories[category] = set()
        self.categories[category].add(acronym_upper)
    
    def remove_acronym(self, acronym: str) -> bool:
        """Remove an acronym from the database"""
        acronym_upper = acronym.upper()
        if acronym_upper in self.acronyms:
            definition = self.acronyms[acronym_upper]
            category = definition.category
            
            # Remove from acronyms
            del self.acronyms[acronym_upper]
            
            # Remove from categories
            if category in self.categories:
                self.categories[category].discard(acronym_upper)
                if not self.categories[category]:
                    del self.categories[category]
            
            return True
        return False
    
    def get_all_acronyms(self) -> List[AcronymDefinition]:
        """Get all acronyms in the database"""
        return list(self.acronyms.values())
    
    def get_categories(self) -> List[str]:
        """Get all categories in the database"""
        return list(self.categories.keys())
    
    def export_to_json(self) -> str:
        """Export database to JSON format"""
        import json
        
        data = {
            "acronyms": {},
            "categories": {}
        }
        
        for acronym, definition in self.acronyms.items():
            data["acronyms"][acronym] = {
                "full_name": definition.full_name,
                "category": definition.category,
                "description": definition.description,
                "is_common": definition.is_common
            }
        
        for category, acronyms in self.categories.items():
            data["categories"][category] = list(acronyms)
        
        return json.dumps(data, indent=2)
    
    def import_from_json(self, json_data: str):
        """Import database from JSON format"""
        import json
        
        data = json.loads(json_data)
        
        # Clear existing data
        self.acronyms.clear()
        self.categories.clear()
        
        # Import acronyms
        for acronym, info in data.get("acronyms", {}).items():
            self.acronyms[acronym] = AcronymDefinition(
                acronym=acronym,
                full_name=info["full_name"],
                category=info["category"],
                description=info.get("description"),
                is_common=info.get("is_common", False)
            )
        
        # Import categories
        for category, acronyms in data.get("categories", {}).items():
            self.categories[category] = set(acronyms)

# Global instance
acronym_db = AcronymDatabase() 