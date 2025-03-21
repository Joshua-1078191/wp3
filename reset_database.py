from lib.database_generator import Base, engine

# Drop all tables
Base.metadata.drop_all(engine)

# Recreate all tables
Base.metadata.create_all(engine)

print("Database tables have been reset.")
