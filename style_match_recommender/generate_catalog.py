import pandas as pd
import os


def generate_fashion_catalog():
    data = [
        [1, "Classic Blue Jeans", "Bottoms", "Casual", "denim durable blue slim fit comfortable"],
        [2, "Slim Fit Denim Jacket", "Outerwear", "Casual", "denim jacket blue classic rugged"],
        [3, "Red Silk Evening Gown", "Dresses", "Formal", "silk red elegant formal long party luxury"],
        [4, "Cotton White T-Shirt", "Tops", "Casual", "cotton white basic plain summer essential"],
        [5, "Leather Biker Jacket", "Outerwear", "Edgy", "leather black jacket warm winter tough style"],
        [6, "Floral Summer Sundress", "Dresses", "Casual", "floral cotton light summer breezy beach"],
        [7, "Black Tailored Blazer", "Outerwear", "Formal", "professional black blazer suit formal office"],
        [8, "Running Performance Shoes", "Footwear", "Sporty", "breathable running lightweight comfort athletic"],
        [9, "Vintage Polka Dot Skirt", "Bottoms", "Vintage", "polka dot skirt retro vintage 50s style"],
        [10, "Cashmere Winter Sweater", "Tops", "Casual", "cashmere wool warm luxury sweater winter soft"],
        [11, "High-Waist Yoga Leggings", "Bottoms", "Sporty", "stretch yoga gym athletic fitness leggings"],
        [12, "Satin Cocktail Dress", "Dresses", "Formal", "satin black short cocktail party dress shiny"],
        [13, "Linen Button-Down Shirt", "Tops", "Casual", "linen breathable summer shirt beach white"],
        [14, "Canvas High-Top Sneakers", "Footwear", "Casual", "canvas sneakers classic white casual daily"],
        [15, "Wool Trench Coat", "Outerwear", "Formal", "wool long trench coat beige winter elegant"],
        [16, "Graphic Print Hoodie", "Tops", "Streetwear", "cotton hoodie graphic print urban streetwear oversized"],
        [17, "Gold Sequined Mini Skirt", "Bottoms", "Party", "gold sequins mini skirt party clubbing shiny"],
        [18, "Velvet Party Blazer", "Outerwear", "Formal", "velvet green blazer luxury formal evening"],
        [19, "Striped Nautical Tee", "Tops", "Casual", "stripes blue white cotton nautical summer"],
        [20, "Leather Chelsea Boots", "Footwear", "Formal", "leather boots black sleek professional formal"],
        # ... and more for variety
    ]

    # Adding more diverse items to reach 50 for better recommendations
    categories = ["Tops", "Bottoms", "Dresses", "Footwear", "Outerwear"]
    styles = ["Casual", "Formal", "Sporty", "Vintage", "Streetwear"]

    # Simple loop to fill the rest with variations
    for i in range(21, 51):
        cat = categories[i % 5]
        style = styles[i % 5]
        data.append([i, f"Product {i}", cat, style, f"{cat.lower()} {style.lower()} stylish trendy comfortable"])

    df = pd.DataFrame(data, columns=['product_id', 'product_name', 'category', 'style', 'description_tags'])

    # Save the file
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/product_catalog.csv', index=False)
    print("Created 'data/product_catalog.csv' with 50 products.")


if __name__ == "__main__":
    generate_fashion_catalog()