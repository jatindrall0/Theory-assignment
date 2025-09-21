import time

class WeatherRecord:
    """A simple class to store weather data for a city in a given year."""
    def __init__(self, year, city, temperature):
        self.year = year
        self.city = city
        self.temperature = temperature


class WeatherDataSystem:
    """Stores weather data using a 2D array (years x cities)."""
    def __init__(self, years, cities):
        self.years = sorted(years)
        self.cities = sorted(cities)

        # Map years and cities to their respective row/column index
        self.year_to_row = {y: i for i, y in enumerate(self.years)}
        self.city_to_col = {c: i for i, c in enumerate(self.cities)}

        # 2D array initialized with None (for missing data)
        rows = len(self.years)
        cols = len(self.cities)
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]

    def insert(self, record):
        """Insert a weather record into the system."""
        if record.year not in self.year_to_row or record.city not in self.city_to_col:
            print(f"-> Could not add record: {record.city} in {record.year} is not tracked.")
            return
        r = self.year_to_row[record.year]
        c = self.city_to_col[record.city]
        self.grid[r][c] = record.temperature
        print(f"-> Added: {record.city}, {record.year} -> {record.temperature}°C")

    def retrieve(self, year, city):
        """Retrieve the temperature for a given city and year."""
        if year not in self.year_to_row or city not in self.city_to_col:
            return "Year or city not tracked."
        r = self.year_to_row[year]
        c = self.city_to_col[city]
        val = self.grid[r][c]
        if val is None:
            return f"No data for {city} in {year}."
        return f"Found: {city} in {year} was {val}°C"

    def delete(self, year, city):
        """Delete a record (set it back to None)."""
        if year not in self.year_to_row or city not in self.city_to_col:
            print("-> Cannot delete: Not found in system.")
            return
        r = self.year_to_row[year]
        c = self.city_to_col[city]
        if self.grid[r][c] is None:
            print(f"-> No data to delete for {city}, {year}.")
        else:
            self.grid[r][c] = None
            print(f"-> Deleted record for {city}, {year}.")

    def row_major_access(self):
        """Scan data row by row (years first, then cities)."""
        print("\n--- Row-Major Scan ---")
        start = time.perf_counter()
        rows, cols = len(self.years), len(self.cities)
        for r in range(rows):
            for c in range(cols):
                _ = self.grid[r][c]
        end = time.perf_counter()
        print(f"Row-major scan took: {end - start:.9f} seconds.")

    def column_major_access(self):
        """Scan data column by column (cities first, then years)."""
        print("\n--- Column-Major Scan ---")
        start = time.perf_counter()
        rows, cols = len(self.years), len(self.cities)
        for c in range(cols):
            for r in range(rows):
                _ = self.grid[r][c]
        end = time.perf_counter()
        print(f"Column-major scan took: {end - start:.9f} seconds.")

    def show_grid(self):
        """Display the current grid of weather data."""
        print("\n--- Weather Data Table ---")
        header = f"{'Year':<8}" + "".join([f"{city:<10}" for city in self.cities])
        print(header)
        print("-" * len(header))
        for i, y in enumerate(self.years):
            row = f"{y:<8}"
            for j in range(len(self.cities)):
                val = self.grid[i][j]
                row += f"{val if val is not None else '---':<10}"
            print(row)
        print("-" * len(header))

    def analyze_complexity(self):
        """Print time and space complexity of operations."""
        print("\n--- Complexity Analysis ---")
        print("- Space: O(Y * C) where Y = years, C = cities")
        print("- Insert/Retrieve/Delete: O(1) average time")
        print("- Row/Column Major Access: O(Y * C) as each cell is visited")


if __name__ == "__main__":
    years_to_track = [2023, 2024, 2025]
    cities_to_track = ["Sohna", "Gurugram", "Faridabad", "Hisar"]

    system = WeatherDataSystem(years_to_track, cities_to_track)
    print("System initialized (grid is empty).")
    system.show_grid()

    print("\n--- Inserting data ---")
    system.insert(WeatherRecord(2023, "Sohna", 28.5))
    system.insert(WeatherRecord(2024, "Gurugram", 30.1))
    system.insert(WeatherRecord(2025, "Faridabad", 31.0))
    system.insert(WeatherRecord(2023, "Hisar", 29.8))
    system.insert(WeatherRecord(2024, "Delhi", 29.5))  # not tracked
    system.show_grid()

    print("\n--- Retrieving data ---")
    print(system.retrieve(2024, "Gurugram"))
    print(system.retrieve(2025, "Sohna"))

    print("\n--- Deleting data ---")
    system.delete(2023, "Hisar")
    system.show_grid()

    system.row_major_access()
    system.column_major_access()
    system.analyze_complexity()
