import csv
import os
csv.field_size_limit(100_000_000)  # In case of large fields

MOVIE_FILE = "C:\\Users\\hp\\OneDrive\\Desktop\\Python Chai\\recommended\\movies_cleaned.csv"

def load_movies_csv(file_path):
    movies = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                movies.append({
                    'title': row['Movie'],
                    'genre': row['Genre'],
                    'total_rating': float(row['TotalRating']),
                    'watch_count': int(row['WatchCount'])
                })
            except:
                continue
    return movies

def save_movies_csv(file_path, movies):
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Movie', 'Genre', 'TotalRating', 'WatchCount'])
        for movie in movies:
            writer.writerow([
                movie['title'],
                movie['genre'],
                round(movie['total_rating'], 2),
                movie['watch_count']
            ])

def recommend_movies(movies, selected_genre):
    filtered = [m for m in movies if selected_genre.lower() in m['genre'].lower()]
    sorted_movies = sorted(filtered, key=lambda m: m['total_rating'] / max(m['watch_count'], 1), reverse=True)
    return sorted_movies[:5]  # Top 5

def update_movie_data(movies, title, new_rating):
    for movie in movies:
        if movie['title'].lower() == title.lower():
            total = movie['total_rating']
            count = movie['watch_count']
            movie['total_rating'] = total + new_rating
            movie['watch_count'] = count + 1
            return True
    return False

def main():
    if not os.path.exists(MOVIE_FILE):
        print(f"❌ File '{MOVIE_FILE}' not found.")
        return
    
    movies = load_movies_csv(MOVIE_FILE)
    print("🎬 Welcome to the Movie Recommendation System!")
    
    genre = input("Enter a genre (e.g., Action, Drama, Comedy): ")
    recommendations = recommend_movies(movies, genre)
    
    if not recommendations:
        print("😕 No movies found for that genre.")
        return
    
    print("\n🎯 Recommended Movies:")
    for idx, movie in enumerate(recommendations, start=1):
        avg_rating = round(movie['total_rating'] / movie['watch_count'], 2) if movie['watch_count'] > 0 else 0
        print(f"{idx}. {movie['title']} — Rating: {avg_rating}/10")
    
    choice = input("\nEnter the number of the movie you watched (or press Enter to skip): ")
    if choice.isdigit():
        choice = int(choice)
        if 1 <= choice <= len(recommendations):
            selected_movie = recommendations[choice - 1]
            try:
                rating = float(input(f"Rate '{selected_movie['title']}' out of 10: "))
                if 0 <= rating <= 10:
                    update_movie_data(movies, selected_movie['title'], rating)
                    save_movies_csv(MOVIE_FILE, movies)
                    print("✅ Thank you! Rating saved.")
                else:
                    print("❌ Please enter a rating between 0 and 10.")
            except ValueError:
                print("❌ Please enter a valid number.")
        else:
            print("❌ Invalid choice.")
    else:
        print("👌 No movie rated this time.")

if __name__ == "__main__":
    main()