# Full transformation script for preparing RAG dataset with clean chunks and structured metadata

import json
import pandas as pd
import os

# Load dataset from file (update the path if needed)
with open(".." + os.path.sep + "dataset" + os.path.sep +"aws_full_dataset.json", "r") as infile:
    threat_entries = json.load(infile)

# Sort by 'Service' key if present
threat_entries.sort(key=lambda x: x.get("Service", ""))

# Function to transform each entry into a RAG-ready chunk + metadata
def format_threats_for_rag(threat_entries):
    rag_ready_data = []
    for entry in threat_entries:
        # Use 'Service' as the target in interaction
        target_service = entry.get("Service", "target service")

        # Use a fixed string for source
        source_entity = "An external client or an AWS service"

        # Handle optional 'Protocol' field
        protocol_text = f" over {entry['Protocol']}" if 'Protocol' in entry and entry['Protocol'] else ""

        chunk = (
            f"Interaction: {source_entity} sends data to {target_service}{protocol_text}\n"
            f"Threat: {entry['Threat Name']}\n"
            f"Description: {entry['Description']}\n"
            f"Mitigation: {entry['Mitigation']}"
        )

        metadata = {
            "threat_id": entry["Threat ID"],
            "threat_name": entry["Threat Name"],
            "source": source_entity,
            "target": target_service
        }
        if 'Protocol' in entry:
            metadata["protocol"] = entry["Protocol"]

        rag_ready_data.append({"text": chunk, "metadata": metadata})
    return rag_ready_data

# Transform the data
rag_dataset = format_threats_for_rag(threat_entries)

final_rag_dataset = os.path.join("..", "aws_rag_dataset.jsonl")

# Save to JSONL for use in embedding pipeline
with open(final_rag_dataset, "w") as f:
    for item in rag_dataset:
        f.write(json.dumps(item) + "\n")

# Preview
for entry in rag_dataset:
    print("\n--- Chunk ---")
    print(entry["text"])
    print("--- Metadata ---")
    print(entry["metadata"])
