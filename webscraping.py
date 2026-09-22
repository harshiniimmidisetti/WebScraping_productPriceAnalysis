# =========================================================
# AMAZON PRODUCT DATA ANALYSIS
# MODULES 4 TO 9
# MENU / SWITCH CASE VERSION
# =========================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import os
import time


# =========================================================
# COLORS FOR TERMINAL
# =========================================================

RESET = "\033[0m"
BOLD = "\033[1m"

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"


# =========================================================
# FILE SETTINGS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

INPUT_FILE = BASE_DIR / "amazon_product.csv"

OUTPUT_DIR = BASE_DIR / "amazon_analysis_outputs"

OUTPUT_DIR.mkdir(exist_ok=True)


# =========================================================
# GLOBAL DATAFRAME
# =========================================================

df = None


# =========================================================
# CLEAR SCREEN
# =========================================================

def clear_screen():

    os.system("cls" if os.name == "nt" else "clear")


# =========================================================
# HEADER
# =========================================================

def print_header(title):

    print("\n" + CYAN + "=" * 70 + RESET)
    print(
        BOLD + YELLOW +
        f"{title:^70}" +
        RESET
    )
    print(CYAN + "=" * 70 + RESET)


# =========================================================
# LOAD DATA
# =========================================================

def load_data():

    global df

    try:

        df = pd.read_csv(INPUT_FILE)

        print(
            GREEN +
            "\nAmazon dataset loaded successfully!" +
            RESET
        )

        print(
            YELLOW +
            f"Dataset Shape: {df.shape}" +
            RESET
        )

        return True

    except FileNotFoundError:

        print(
            RED +
            "\nERROR: amazon_product.csv was not found!" +
            RESET
        )

        print(
            YELLOW +
            f"Expected location:\n{INPUT_FILE}" +
            RESET
        )

        return False


# =========================================================
# MODULE 1
# DISPLAY AMAZON DATASET
# =========================================================

def display_dataset():

    global df

    print_header("AMAZON PRODUCT DATASET")

    if df is None:

        if not load_data():

            return

    print(
        GREEN +
        "\nAMAZON PRODUCT DATASET" +
        RESET
    )

    print(
        BLUE +
        "-" * 70 +
        RESET
    )

    print(
        YELLOW +
        f"Number of Rows    : {df.shape[0]}" +
        RESET
    )

    print(
        YELLOW +
        f"Number of Columns : {df.shape[1]}" +
        RESET
    )

    print(
        BLUE +
        "-" * 70 +
        RESET
    )

    print(
        MAGENTA +
        "\nCOLUMN NAMES:" +
        RESET
    )

    for i, column in enumerate(df.columns, 1):

        print(
            CYAN +
            f"{i:2}. {column}" +
            RESET
        )

    print(
        MAGENTA +
        "\nFIRST 10 RECORDS:" +
        RESET
    )

    print(
        GREEN +
        df.head(10).to_string(index=False) +
        RESET
    )

    print(
        MAGENTA +
        "\nDATA TYPES:" +
        RESET
    )

    print(
        YELLOW +
        df.dtypes.to_string() +
        RESET
    )

    print(
        GREEN +
        "\nDataset displayed successfully!" +
        RESET
    )


# =========================================================
# MODULE 4
# DATA PREPROCESSING
# =========================================================

def data_preprocessing():

    global df

    print_header("MODULE 4: DATA PREPROCESSING")

    if df is None:

        if not load_data():

            return

    # -----------------------------------------------------
    # Remove unnecessary column
    # -----------------------------------------------------

    if "Unnamed: 0" in df.columns:

        df = df.drop(
            columns=["Unnamed: 0"]
        )

        print(
            GREEN +
            "\nUnnecessary index column removed." +
            RESET
        )

    # -----------------------------------------------------
    # Convert price fields
    # -----------------------------------------------------

    price_columns = [

        "product_price",
        "product_original_price",
        "product_minimum_offer_price",
        "unit_price"

    ]

    print(
        YELLOW +
        "\nConverting price fields to numeric..." +
        RESET
    )

    for col in price_columns:

        if col in df.columns:

            df[col] = pd.to_numeric(

                df[col]
                .astype(str)
                .str.replace(
                    r"[$,]",
                    "",
                    regex=True
                ),

                errors="coerce"

            )

    print(
        GREEN +
        "Price conversion completed." +
        RESET
    )

    # -----------------------------------------------------
    # Numeric columns
    # -----------------------------------------------------

    numeric_columns = [

        "product_star_rating",
        "product_num_ratings",
        "product_num_offers",
        "unit_count"

    ]

    for col in numeric_columns:

        if col in df.columns:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    print(
        GREEN +
        "Numeric attributes converted." +
        RESET
    )

    # -----------------------------------------------------
    # Clean text columns
    # -----------------------------------------------------

    text_columns = [

        "product_title",
        "currency",
        "sales_volume",
        "delivery",
        "product_availability"

    ]

    for col in text_columns:

        if col in df.columns:

            df[col] = (
                df[col]
                .astype("string")
                .str.strip()
            )

    print(
        GREEN +
        "Text columns cleaned." +
        RESET
    )

    # -----------------------------------------------------
    # Remove duplicate ASIN
    # -----------------------------------------------------

    if "asin" in df.columns:

        before = len(df)

        df = df.drop_duplicates(
            subset="asin",
            keep="first"
        )

        removed = before - len(df)

        print(
            GREEN +
            f"Duplicate ASIN rows removed: {removed}" +
            RESET
        )

    # -----------------------------------------------------
    # Free products
    # -----------------------------------------------------

    df["is_free_product"] = (

        df["product_price"]
        .fillna(0)
        .eq(0)

    )

    # -----------------------------------------------------
    # Discount amount
    # -----------------------------------------------------

    df["discount_amount"] = (

        df["product_original_price"]
        -
        df["product_price"]

    )

    # -----------------------------------------------------
    # Discount percentage
    # -----------------------------------------------------

    valid_discount = (

        df["product_original_price"].gt(0)

        &

        df["product_price"].ge(0)

        &

        df["product_original_price"]
        .ge(df["product_price"])

    )

    df["discount_percentage"] = np.where(

        valid_discount,

        (
            df["discount_amount"]
            /
            df["product_original_price"]
        ) * 100,

        np.nan

    )

    # -----------------------------------------------------
    # Offer saving
    # -----------------------------------------------------

    df["offer_saving"] = (

        df["product_price"]
        -
        df["product_minimum_offer_price"]

    )

    # =====================================================
    # DATA QUALITY
    # =====================================================

    print_header("DATA QUALITY CHECK")

    print(
        YELLOW +
        "\nMissing Values:" +
        RESET
    )

    print(
        df.isna().sum()
    )

    print(
        YELLOW +
        "\nDuplicate Rows:" +
        RESET
    )

    print(
        df.duplicated().sum()
    )

    # -----------------------------------------------------
    # Invalid ratings
    # -----------------------------------------------------

    invalid_rating = (

        df["product_star_rating"].notna()

        &

        ~df["product_star_rating"]
        .between(0, 5)

    )

    df["invalid_rating"] = invalid_rating

    print(
        YELLOW +
        "\nInvalid ratings:" +
        RESET,
        int(df["invalid_rating"].sum())
    )

    # =====================================================
    # IQR OUTLIER DETECTION
    # =====================================================

    def add_iqr_outlier_flag(
        data,
        column,
        flag_name
    ):

        Q1 = data[column].quantile(0.25)

        Q3 = data[column].quantile(0.75)

        IQR = Q3 - Q1

        lower_limit = Q1 - 1.5 * IQR

        upper_limit = Q3 + 1.5 * IQR

        data[flag_name] = (

            data[column].notna()

            &

            (
                (data[column] < lower_limit)

                |

                (data[column] > upper_limit)
            )

        )

        return (
            Q1,
            Q3,
            IQR,
            lower_limit,
            upper_limit
        )

    # -----------------------------------------------------
    # Price outliers
    # -----------------------------------------------------

    price_stats = add_iqr_outlier_flag(

        df,

        "product_price",

        "price_outlier"

    )

    print_header("PRICE OUTLIER ANALYSIS")

    print(
        "Q1:",
        price_stats[0]
    )

    print(
        "Q3:",
        price_stats[1]
    )

    print(
        "IQR:",
        price_stats[2]
    )

    print(
        "Lower Limit:",
        price_stats[3]
    )

    print(
        "Upper Limit:",
        price_stats[4]
    )

    print(
        RED +
        "Price Outliers:" +
        RESET,
        int(df["price_outlier"].sum())
    )

    # -----------------------------------------------------
    # Rating count outliers
    # -----------------------------------------------------

    rating_count_stats = add_iqr_outlier_flag(

        df,

        "product_num_ratings",

        "rating_count_outlier"

    )

    print_header("RATING COUNT OUTLIER ANALYSIS")

    print(
        "Q1:",
        rating_count_stats[0]
    )

    print(
        "Q3:",
        rating_count_stats[1]
    )

    print(
        "IQR:",
        rating_count_stats[2]
    )

    print(
        "Lower Limit:",
        rating_count_stats[3]
    )

    print(
        "Upper Limit:",
        rating_count_stats[4]
    )

    print(
        RED +
        "Rating Count Outliers:" +
        RESET,
        int(df["rating_count_outlier"].sum())
    )

    # -----------------------------------------------------
    # SAVE CLEANED DATA
    # -----------------------------------------------------

    cleaned_file = (

        OUTPUT_DIR /
        "amazon_products_cleaned.csv"

    )

    df.to_csv(
        cleaned_file,
        index=False
    )

    print(
        GREEN +
        "\nCleaned dataset saved successfully!" +
        RESET
    )

    print(
        CYAN +
        f"Location: {cleaned_file}" +
        RESET
    )

    print(
        YELLOW +
        f"Cleaned Dataset Shape: {df.shape}" +
        RESET
    )


# =========================================================
# MODULE 5
# EXPLORATORY DATA ANALYSIS
# =========================================================

def exploratory_data_analysis():

    global df

    print_header(
        "MODULE 5: EXPLORATORY DATA ANALYSIS"
    )

    if df is None:

        if not load_data():

            return

    print(
        MAGENTA +
        "\nPRICE DISTRIBUTION" +
        RESET
    )

    print(
        df["product_price"].describe()
    )

    print(
        MAGENTA +
        "\nRATING DISTRIBUTION" +
        RESET
    )

    print(
        df["product_star_rating"].describe()
    )

    print(
        MAGENTA +
        "\nPRODUCT ATTRIBUTE ANALYSIS" +
        RESET
    )

    if "is_best_seller" in df.columns:

        print(
            "Best Sellers:",
            int(df["is_best_seller"].sum())
        )

    if "is_amazon_choice" in df.columns:

        print(
            "Amazon Choice:",
            int(df["is_amazon_choice"].sum())
        )

    if "is_prime" in df.columns:

        print(
            "Prime Products:",
            int(df["is_prime"].sum())
        )

    if "has_variations" in df.columns:

        print(
            "Products with Variations:",
            int(df["has_variations"].sum())
        )

    if "is_free_product" in df.columns:

        print(
            "Free Products:",
            int(df["is_free_product"].sum())
        )


# =========================================================
# MODULE 6
# PRODUCT ANALYSIS
# =========================================================

def product_analysis():

    global df

    print_header(
        "MODULE 6: PRODUCT ANALYSIS"
    )

    if df is None:

        if not load_data():

            return

    # -----------------------------------------------------
    # Current vs original price
    # -----------------------------------------------------

    priced_products = df[

        df["product_original_price"].notna()

        &

        df["product_price"].notna()

    ]

    print(
        "\nProducts with original price:",
        len(priced_products)
    )

    print(
        "Average Current Price: $",
        round(
            df["product_price"].mean(),
            2
        )
    )

    print(
        "Average Original Price: $",
        round(
            priced_products[
                "product_original_price"
            ].mean(),
            2
        )
    )

    # -----------------------------------------------------
    # Discount
    # -----------------------------------------------------

    print(
        "\nAverage Discount Percentage:",
        round(
            df["discount_percentage"].mean(),
            2
        ),
        "%"
    )

    print(
        MAGENTA +
        "\nTOP 10 PRODUCTS BY DISCOUNT" +
        RESET
    )

    top_discount = (

        df.sort_values(
            "discount_percentage",
            ascending=False
        )

        [[
            "product_title",
            "product_price",
            "product_original_price",
            "discount_percentage"
        ]]

        .head(10)

    )

    print(
        top_discount.to_string(
            index=False
        )
    )

    # -----------------------------------------------------
    # Offers
    # -----------------------------------------------------

    print(
        "\nAverage Number of Offers:",
        round(
            df["product_num_offers"].mean(),
            2
        )
    )

    # -----------------------------------------------------
    # Ratings
    # -----------------------------------------------------

    print(
        "\nAverage Product Rating:",
        round(
            df["product_star_rating"].mean(),
            2
        )
    )

    print(
        "Average Number of Ratings:",
        round(
            df["product_num_ratings"].mean(),
            2
        )
    )

    # -----------------------------------------------------
    # Top reviewed products
    # -----------------------------------------------------

    print(
        MAGENTA +
        "\nTOP 10 PRODUCTS BY NUMBER OF RATINGS" +
        RESET
    )

    top_reviews = (

        df.sort_values(
            "product_num_ratings",
            ascending=False
        )

        [[
            "product_title",
            "product_star_rating",
            "product_num_ratings",
            "product_price"
        ]]

        .head(10)

    )

    print(
        top_reviews.to_string(
            index=False
        )
    )


# =========================================================
# MODULE 7
# STATISTICAL ANALYSIS
# =========================================================

def statistical_analysis():

    global df

    print_header(
        "MODULE 7: STATISTICAL ANALYSIS"
    )

    if df is None:

        if not load_data():

            return

    # -----------------------------------------------------
    # PRICE STATISTICS
    # -----------------------------------------------------

    print(
        MAGENTA +
        "\nPRICE STATISTICS" +
        RESET
    )

    print(
        "Average:",
        round(
            df["product_price"].mean(),
            2
        )
    )

    print(
        "Minimum:",
        round(
            df["product_price"].min(),
            2
        )
    )

    print(
        "Maximum:",
        round(
            df["product_price"].max(),
            2
        )
    )

    print(
        "Median:",
        round(
            df["product_price"].median(),
            2
        )
    )

    print(
        "Standard Deviation:",
        round(
            df["product_price"].std(),
            2
        )
    )

    # -----------------------------------------------------
    # RATING STATISTICS
    # -----------------------------------------------------

    print(
        MAGENTA +
        "\nRATING STATISTICS" +
        RESET
    )

    print(
        "Average:",
        round(
            df["product_star_rating"].mean(),
            2
        )
    )

    print(
        "Minimum:",
        round(
            df["product_star_rating"].min(),
            2
        )
    )

    print(
        "Maximum:",
        round(
            df["product_star_rating"].max(),
            2
        )
    )

    print(
        "Median:",
        round(
            df["product_star_rating"].median(),
            2
        )
    )

    print(
        "Standard Deviation:",
        round(
            df["product_star_rating"].std(),
            2
        )
    )

    # -----------------------------------------------------
    # NUMPY
    # -----------------------------------------------------

    price_array = (

        df["product_price"]
        .dropna()
        .to_numpy()

    )

    rating_array = (

        df["product_star_rating"]
        .dropna()
        .to_numpy()

    )

    print(
        MAGENTA +
        "\nNUMPY CALCULATIONS" +
        RESET
    )

    print(
        "NumPy Price Mean:",
        round(
            np.mean(price_array),
            2
        )
    )

    print(
        "NumPy Price Minimum:",
        round(
            np.min(price_array),
            2
        )
    )

    print(
        "NumPy Price Maximum:",
        round(
            np.max(price_array),
            2
        )
    )

    print(
        "NumPy Rating Mean:",
        round(
            np.mean(rating_array),
            2
        )
    )

    # -----------------------------------------------------
    # PRICE CATEGORY
    # -----------------------------------------------------

    df["price_category"] = pd.cut(

        df["product_price"],

        bins=[
            -np.inf,
            50,
            150,
            300,
            np.inf
        ],

        labels=[
            "Low (<=50)",
            "Medium (51-150)",
            "High (151-300)",
            "Premium (>300)"
        ]

    )

    print(
        MAGENTA +
        "\nPRICE CATEGORY DISTRIBUTION" +
        RESET
    )

    print(
        df["price_category"]
        .value_counts()
        .sort_index()
    )


# =========================================================
# MODULE 8
# VISUALIZATION
# =========================================================

def visualization():

    global df

    print_header(
        "MODULE 8: VISUALIZATION"
    )

    if df is None:

        if not load_data():

            return

    # -----------------------------------------------------
    # 1. PRICE HISTOGRAM
    # -----------------------------------------------------

    plt.figure(figsize=(9, 5))

    plt.hist(
        df["product_price"].dropna(),
        bins=12,
        edgecolor="black"
    )

    plt.title(
        "Product Price Distribution"
    )

    plt.xlabel(
        "Price (USD)"
    )

    plt.ylabel(
        "Number of Products"
    )

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR /
        "01_price_distribution.png",
        dpi=300
    )

    plt.show()

    # -----------------------------------------------------
    # 2. RATING HISTOGRAM
    # -----------------------------------------------------

    plt.figure(figsize=(9, 5))

    plt.hist(
        df["product_star_rating"].dropna(),
        bins=10,
        edgecolor="black"
    )

    plt.title(
        "Product Rating Distribution"
    )

    plt.xlabel(
        "Rating"
    )

    plt.ylabel(
        "Number of Products"
    )

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR /
        "02_rating_distribution.png",
        dpi=300
    )

    plt.show()

    # -----------------------------------------------------
    # 3. PRICE CATEGORY BAR
    # -----------------------------------------------------

    if "price_category" not in df.columns:

        df["price_category"] = pd.cut(

            df["product_price"],

            bins=[
                -np.inf,
                50,
                150,
                300,
                np.inf
            ],

            labels=[
                "Low (<=50)",
                "Medium (51-150)",
                "High (151-300)",
                "Premium (>300)"
            ]

        )

    price_counts = (

        df["price_category"]
        .value_counts()
        .sort_index()

    )

    plt.figure(figsize=(9, 5))

    plt.bar(
        price_counts.index.astype(str),
        price_counts.values
    )

    plt.title(
        "Products by Price Category"
    )

    plt.xlabel(
        "Price Category"
    )

    plt.ylabel(
        "Number of Products"
    )

    plt.xticks(
        rotation=15
    )

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR /
        "03_price_category_bar.png",
        dpi=300
    )

    plt.show()

    # -----------------------------------------------------
    # 4. PRICE VS RATING
    # -----------------------------------------------------

    plt.figure(figsize=(9, 5))

    plt.scatter(

        df["product_price"],

        df["product_star_rating"],

        alpha=0.7

    )

    plt.title(
        "Price vs Product Rating"
    )

    plt.xlabel(
        "Price (USD)"
    )

    plt.ylabel(
        "Rating"
    )

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR /
        "04_price_vs_rating_scatter.png",
        dpi=300
    )

    plt.show()

    # -----------------------------------------------------
    # 5. CURRENT VS ORIGINAL PRICE
    # -----------------------------------------------------

    comparison = (

        df.dropna(
            subset=[
                "product_price",
                "product_original_price"
            ]
        )

        .head(15)

    )

    x = np.arange(
        len(comparison)
    )

    width = 0.35

    plt.figure(figsize=(12, 6))

    plt.bar(

        x - width / 2,

        comparison[
            "product_original_price"
        ],

        width,

        label="Original Price"

    )

    plt.bar(

        x + width / 2,

        comparison[
            "product_price"
        ],

        width,

        label="Current Price"

    )

    plt.title(
        "Current Price vs Original Price"
    )

    plt.xlabel(
        "Selected Products"
    )

    plt.ylabel(
        "Price (USD)"
    )

    plt.xticks(
        x,
        range(
            1,
            len(comparison) + 1
        )
    )

    plt.legend()

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR /
        "05_current_vs_original_price.png",
        dpi=300
    )

    plt.show()

    # -----------------------------------------------------
    # 6. RATINGS VS REVIEW COUNT
    # -----------------------------------------------------

    plt.figure(figsize=(9, 5))

    plt.scatter(

        df["product_num_ratings"],

        df["product_star_rating"],

        alpha=0.7

    )

    plt.title(
        "Number of Ratings vs Product Rating"
    )

    plt.xlabel(
        "Number of Ratings"
    )

    plt.ylabel(
        "Product Rating"
    )

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR /
        "06_ratings_vs_review_count.png",
        dpi=300
    )

    plt.show()

    print(
        GREEN +
        "\nAll 6 graphs generated successfully!" +
        RESET
    )

    print(
        CYAN +
        f"Graphs saved in: {OUTPUT_DIR}" +
        RESET
    )


# =========================================================
# MODULE 9
# INSIGHT GENERATION
# =========================================================

def insight_generation():

    global df

    print_header(
        "MODULE 9: INSIGHT GENERATION"
    )

    if df is None:

        if not load_data():

            return

    # -----------------------------------------------------
    # Pricing pattern
    # -----------------------------------------------------

    non_free = df[
        df["product_price"] > 0
    ]

    print(
        MAGENTA +
        "\n1. PRICING PATTERN" +
        RESET
    )

    print(
        f"Non-free product prices range from "
        f"${non_free['product_price'].min():.2f} "
        f"to "
        f"${non_free['product_price'].max():.2f}."
    )

    print(
        "Free-priced products:",
        int(
            df["is_free_product"].sum()
        )
    )

    # -----------------------------------------------------
    # Offer pattern
    # -----------------------------------------------------

    discounted = df[
        df["discount_percentage"] > 0
    ]

    print(
        MAGENTA +
        "\n2. OFFER / PROMOTION PATTERN" +
        RESET
    )

    print(
        f"{len(discounted)} products have "
        "a calculated discount."
    )

    if len(discounted) > 0:

        print(
            "Average calculated discount:",
            round(
                discounted[
                    "discount_percentage"
                ].mean(),
                2
            ),
            "%"
        )

    # -----------------------------------------------------
    # Rating pattern
    # -----------------------------------------------------

    print(
        MAGENTA +
        "\n3. RATING PATTERN" +
        RESET
    )

    print(
        "Average Rating:",
        round(
            df["product_star_rating"].mean(),
            2
        )
    )

    print(
        "Products with missing ratings:",
        int(
            df["product_star_rating"]
            .isna()
            .sum()
        )
    )

    # -----------------------------------------------------
    # Product attributes
    # -----------------------------------------------------

    print(
        MAGENTA +
        "\n4. PRODUCT ATTRIBUTES" +
        RESET
    )

    if "is_best_seller" in df.columns:

        print(
            "Best Seller Products:",
            int(
                df["is_best_seller"].sum()
            )
        )

    if "is_amazon_choice" in df.columns:

        print(
            "Amazon Choice Products:",
            int(
                df["is_amazon_choice"].sum()
            )
        )

    if "is_prime" in df.columns:

        print(
            "Prime Products:",
            int(
                df["is_prime"].sum()
            )
        )

    # -----------------------------------------------------
    # Most reviewed product
    # -----------------------------------------------------

    print(
        MAGENTA +
        "\n5. PRODUCT-LEVEL INSIGHT" +
        RESET
    )

    valid_reviews = df[
        df["product_num_ratings"].notna()
    ]

    if len(valid_reviews) > 0:

        top_product = valid_reviews.loc[
            valid_reviews[
                "product_num_ratings"
            ].idxmax()
        ]

        print(
            "Most Reviewed Product:",
            top_product[
                "product_title"
            ]
        )

        print(
            "Number of Ratings:",
            int(
                top_product[
                    "product_num_ratings"
                ]
            )
        )

        print(
            "Product Rating:",
            top_product[
                "product_star_rating"
            ]
        )

        print(
            "Current Price:",
            top_product[
                "product_price"
            ]
        )


# =========================================================
# COMPLETE ANALYSIS
# =========================================================

def complete_analysis():

    print_header(
        "COMPLETE AMAZON PRODUCT ANALYSIS"
    )

    if df is None:

        if not load_data():

            return

    data_preprocessing()

    exploratory_data_analysis()

    product_analysis()

    statistical_analysis()

    visualization()

    insight_generation()

    print_header(
        "COMPLETE ANALYSIS FINISHED"
    )

    print(
        GREEN +
        "All Modules 4 to 9 completed successfully!" +
        RESET
    )


# =========================================================
# MAIN MENU
# =========================================================

def main_menu():

    while True:

        print_header(
            "AMAZON PRODUCT DATA ANALYSIS"
        )

        print(
            GREEN +
            "\n1. Display Amazon Dataset" +
            RESET
        )

        print(
            YELLOW +
            "2. Data Preprocessing" +
            RESET
        )

        print(
            CYAN +
            "3. Exploratory Data Analysis" +
            RESET
        )

        print(
            MAGENTA +
            "4. Product Analysis" +
            RESET
        )

        print(
            BLUE +
            "5. Statistical Analysis" +
            RESET
        )

        print(
            RED +
            "6. Visualization" +
            RESET
        )

        print(
            GREEN +
            "7. Insight Generation" +
            RESET
        )

        print(
            YELLOW +
            "8. Run Complete Analysis" +
            RESET
        )

        print(
            RED +
            "0. Exit" +
            RESET
        )

        print(
            CYAN +
            "-" * 70 +
            RESET
        )

        choice = input(
            BOLD +
            "Enter your choice: " +
            RESET
        )

        # =================================================
        # SWITCH CASE
        # =================================================

        match choice:

            case "1":

                clear_screen()

                display_dataset()

                input(
                    "\nPress ENTER to return to menu..."
                )

            case "2":

                clear_screen()

                data_preprocessing()

                input(
                    "\nPress ENTER to return to menu..."
                )

            case "3":

                clear_screen()

                exploratory_data_analysis()

                input(
                    "\nPress ENTER to return to menu..."
                )

            case "4":

                clear_screen()

                product_analysis()

                input(
                    "\nPress ENTER to return to menu..."
                )

            case "5":

                clear_screen()

                statistical_analysis()

                input(
                    "\nPress ENTER to return to menu..."
                )

            case "6":

                clear_screen()

                visualization()

                input(
                    "\nPress ENTER to return to menu..."
                )

            case "7":

                clear_screen()

                insight_generation()

                input(
                    "\nPress ENTER to return to menu..."
                )

            case "8":

                clear_screen()

                complete_analysis()

                input(
                    "\nPress ENTER to return to menu..."
                )

            case "0":

                print(
                    GREEN +
                    "\nThank you for using Amazon Product "
                    "Data Analysis!" +
                    RESET
                )

                print(
                    CYAN +
                    "Program exited successfully." +
                    RESET
                )

                break

            case _:

                print(
                    RED +
                    "\nInvalid choice!" +
                    RESET
                )

                print(
                    YELLOW +
                    "Please enter a number from 0 to 8." +
                    RESET
                )

                time.sleep(2)


# =========================================================
# PROGRAM START
# =========================================================

if __name__ == "__main__":

    main_menu()