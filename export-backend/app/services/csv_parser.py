import pandas as pd


def process_bolt_data(df: pd.DataFrame) -> pd.DataFrame:
    print(df)

    # Clean column names
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace("|", "_", regex=False)
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    # Convert 'datum' to datetime
    df["datum"] = pd.to_datetime(df["datum"], errors="coerce")

    # Convert numeric columns to floats
    numeric_columns = [
        "entfernung_km",
        "trinkgeld_€",
        "fahrtpreis_€",
        "buchungsgebühr_€",
        "mautgebühr_€",
        "stornogebühr_€",
    ]
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Filter only completed rides
    df = df[df["status"] == "Abgeschlossen"]

    # TODO: Choose which fields to keep in df
    df = df[
        [
            "datum",
            "fahrer",
            "fahrer_telefonnummer",
            "fahrtpreis_€",
            "trinkgeld_€",
            "status",
        ]
    ]

    return df
