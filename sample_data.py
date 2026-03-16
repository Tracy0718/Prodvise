from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class User:
    id: str
    name: str
    age: int
    preferences: List[str]
    ratings: Dict[str, int]
    avatar: Optional[str] = None
    location: Optional[str] = None
    joined_date: Optional[str] = None
    email: Optional[str] = None

@dataclass
class Product:
    id: str
    title: str
    category: str
    description: str
    features: List[str]
    average_rating: float
    total_ratings: int
    price: float
    image_url: str
    brand: Optional[str] = None
    in_stock: Optional[bool] = None
    shipping: Optional[str] = None
    tags: Optional[List[str]] = field(default_factory=list)

sample_users = [
    User(
        id="u1",
        name="Alice Johnson",
        age=28,
        preferences=["technology", "books", "fitness"],
        avatar="https://randomuser.me/api/portraits/women/44.jpg",
        location="San Francisco, CA",
        joined_date="2023-06-15",
        ratings={"p1": 5, "p2": 4, "p3": 3, "p7": 5, "p8": 4}
    ),
    User(
        id="u2",
        name="Bob Smith",
        age=35,
        preferences=["technology", "gaming", "music"],
        avatar="https://randomuser.me/api/portraits/men/32.jpg",
        location="New York, NY",
        joined_date="2023-03-22",
        ratings={"p1": 4, "p4": 5, "p5": 3}
    ),
    User(
        id="u3",
        name="Carol Davis",
        age=42,
        preferences=["books", "fitness", "cooking"],
        avatar="https://randomuser.me/api/portraits/women/68.jpg",
        location="Austin, TX",
        joined_date="2023-01-10",
        ratings={"p2": 5, "p3": 4, "p6": 5}
    ),
    User(
        id="u4",
        name="David Wilson",
        age=31,
        preferences=["gaming", "technology", "movies"],
        avatar="https://randomuser.me/api/portraits/men/65.jpg",
        location="Seattle, WA",
        joined_date="2023-08-05",
        ratings={"p4": 4, "p5": 5, "p1": 3}
    ),
    User(
        id="u5",
        name="Eva Brown",
        age=26,
        preferences=["fitness", "books", "travel"],
        avatar="https://randomuser.me/api/portraits/women/12.jpg",
        location="Denver, CO",
        joined_date="2023-11-12",
        ratings={"p3": 5, "p6": 4, "p7": 3}
    ),
]

sample_products = [
    Product(
        id="p1",
        title="MacBook Pro 16\"",
        category="technology",
        description="High-performance laptop with M2 Pro chip, perfect for developers and creators with exceptional performance and stunning display",
        features=["M2 Pro chip", "16GB RAM", "512GB SSD", "Retina display"],
        average_rating=4.5,
        total_ratings=127,
        price=2499,
        image_url="macbook-pro.jpg",
        brand="Apple",
        in_stock=True,
        shipping="Free shipping",
        tags=["laptop", "pro", "development", "creative"]
    ),
    Product(
        id="p2",
        title="The Psychology of Computer Programming",
        category="books",
        description="Classic book on software development psychology and team dynamics by Gerald M. Weinberg",
        features=["Software engineering", "Psychology", "Team management"],
        average_rating=4.7,
        total_ratings=89,
        price=39,
        image_url="psychology-book.jpg",
        brand="Dorset House",
        in_stock=True,
        shipping="Free shipping",
        tags=["programming", "psychology", "software", "classic"]
    ),
    Product(
        id="p3",
        title="Yoga Mat Premium",
        category="fitness",
        description="Non-slip yoga mat made from eco-friendly materials with superior grip and comfort",
        features=["Eco-friendly", "Non-slip", "6mm thick", "Lightweight"],
        average_rating=4.3,
        total_ratings=156,
        price=79,
        image_url="yoga-mat.jpg",
        brand="EcoYoga",
        in_stock=True,
        shipping="Free shipping",
        tags=["yoga", "fitness", "eco-friendly", "exercise"]
    ),
    Product(
        id="p4",
        title="PlayStation 5",
        category="gaming",
        description="Next-generation gaming console with 4K graphics and ray tracing for immersive gaming experience",
        features=["4K gaming", "Ray tracing", "SSD storage", "Haptic feedback"],
        average_rating=4.8,
        total_ratings=234,
        price=499,
        image_url="playstation-5.jpg",
        brand="Sony",
        in_stock=False,
        shipping="Free shipping",
        tags=["gaming", "console", "4K", "entertainment"]
    ),
    Product(
        id="p5",
        title="Mechanical Gaming Keyboard",
        category="gaming",
        description="RGB backlit mechanical keyboard with Cherry MX switches for competitive gaming",
        features=["Cherry MX switches", "RGB backlight", "Programmable keys"],
        average_rating=4.4,
        total_ratings=98,
        price=149,
        image_url="gaming-keyboard.jpg",
        brand="Corsair",
        in_stock=True,
        shipping="Free shipping",
        tags=["keyboard", "gaming", "mechanical", "RGB"]
    ),
    Product(
        id="p6",
        title="Resistance Bands Set",
        category="fitness",
        description="Complete set of resistance bands for home workouts with varying resistance levels",
        features=["Multiple resistance levels", "Portable", "Exercise guide included"],
        average_rating=4.2,
        total_ratings=76,
        price=29,
        image_url="resistance-bands.jpg",
        brand="FitnessPro",
        in_stock=True,
        shipping="Free shipping",
        tags=["fitness", "resistance", "workout", "portable"]
    ),
    Product(
        id="p7",
        title="Clean Code",
        category="books",
        description="A handbook of agile software craftsmanship by Robert C. Martin - essential for every developer",
        features=["Software engineering", "Best practices", "Code quality"],
        average_rating=4.6,
        total_ratings=203,
        price=45,
        image_url="clean-code-book.jpg",
        brand="Prentice Hall",
        in_stock=True,
        shipping="Free shipping",
        tags=["programming", "clean code", "software", "development"]
    ),
    Product(
        id="p8",
        title="iPhone 15 Pro",
        category="technology",
        description="Latest iPhone with titanium design and A17 Pro chip for professional photography and performance",
        features=["A17 Pro chip", "Titanium design", "Pro camera system"],
        average_rating=4.5,
        total_ratings=189,
        price=999,
        image_url="iphone-15-pro.jpg",
        brand="Apple",
        in_stock=True,
        shipping="Free shipping",
        tags=["smartphone", "pro", "camera", "titanium"]
    ),
] 