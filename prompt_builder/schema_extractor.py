import sqlite3
import sys
from datetime import datetime

def extract_schema_to_markdown(db_path='db.sqlite3', output_file='database_schema.md'):
    """
    Extracts schema for all tables in a SQLite database and writes to a Markdown file.
    """
    try:
        conn = sqlite3.connect(db_path)
        db_cursor = conn.cursor()
        
        db_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        tables = db_cursor.fetchall()
        
        if not tables:
            print("No tables found in the database.")
            return
        
        # Open markdown file for writing
        with open(output_file, 'w', encoding='utf-8') as f:
            # Write header
            f.write(f"# Database Schema\n\n")
            f.write(f"**Database:** `{db_path}`  \n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  \n")
            f.write(f"**Total Tables:** {len(tables)}\n\n")
            
            # Table of contents
            f.write("## Table of Contents\n\n")
            for table_tuple in tables:
                table_name = table_tuple[0]
                f.write(f"- [{table_name}](#{table_name.lower().replace('_', '-')})\n")
            f.write("\n---\n\n")
            
            # For each table, write detailed schema
            for table_tuple in tables:
                table_name = table_tuple[0]
                f.write(f"## {table_name}\n\n")
                
                # Get column information
                db_cursor.execute(f"PRAGMA table_info({table_name});")
                columns = db_cursor.fetchall()
                
                if columns:
                    # Write table header
                    f.write("| Column Name | Type | Nullable | Default | Primary Key |\n")
                    f.write("|-------------|------|----------|---------|-------------|\n")
                    
                    # Write column rows
                    for col in columns:
                        cid, name, col_type, not_null, default_val, pk = col
                        null_str = "❌" if not_null else "✅"
                        default_str = f"`{default_val}`" if default_val is not None else "-"
                        pk_str = "🔑" if pk else "-"
                        
                        f.write(f"| `{name}` | {col_type} | {null_str} | {default_str} | {pk_str} |\n")
                
                # Get row count
                db_cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
                row_count = db_cursor.fetchone()[0]
                f.write(f"\n**Total Rows:** {row_count}\n\n")
                
                # Get CREATE TABLE statement
                db_cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}';")
                create_stmt = db_cursor.fetchone()
                if create_stmt and create_stmt[0]:
                    f.write("### CREATE Statement\n\n")
                    f.write("```sql\n")
                    f.write(f"{create_stmt[0]}\n")
                    f.write("```\n\n")
                
                f.write("---\n\n")
        
        conn.close()
        print(f"✅ Schema successfully written to: {output_file}")
        
    except sqlite3.Error as e:
        print(f"❌ SQLite error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    db_path = sys.argv[1] if len(sys.argv) > 1 else 'db.sqlite3'
    output_file = 'prompt_builder/database_schema.md'
    extract_schema_to_markdown(db_path, output_file)