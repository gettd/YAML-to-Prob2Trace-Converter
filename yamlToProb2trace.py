import yaml
import json
from pathlib import Path

def extract_ego_position(state):
    ego = state.get("groundtruth_ego", {})
    pos = ego.get("pose", {}).get("position", {})
    return (
        pos.get("x", 0),
        pos.get("y", 0),
        pos.get("z", 0)
    )

def extract_npc_position(state):
    npcs = state.get("groundtruth_NPCs", [])
    for npc in npcs:
        if npc.get("name") == "npc1":
            pos = npc.get("pose", {}).get("position", {})
            return (
                pos.get("x", 0),
                pos.get("y", 0),
                pos.get("z", 0)
            )
    return None

def extract_npc_perceived(state):
    npcs = state.get("perception_objects", [])
    if not npcs:
        return None
    for npc in npcs:
        pos = npc.get("pose", {}).get("position", {})
        return (
            pos.get("x", 0),
            pos.get("y", 0),
            pos.get("z", 0)
        )
    return None

def yaml_to_prob2trace_format(yaml_file, output_file):
    with open(yaml_file, 'r') as f:
        yaml_data = yaml.safe_load(f)

    states = yaml_data.get("states", [])
    if not states:
        raise ValueError("No states found in YAML.")

    transitions = []

    last_timestamp = states[-1].get("timeStamp", 0)
    transitions.append({
        "name": "$setup_constants",
        "params": None,
        "results": None,
        "destState": {
            "timeStampMAX": str(last_timestamp)
        },
        "destStateNotChanged": [],
        "preds": None
    })

    #init first state
    first_state = states[0]
    ego_pos = extract_ego_position(first_state)
    npc_pos = extract_npc_position(first_state)
    perceived_pos = extract_npc_perceived(first_state)
    timestamp_scaled = first_state.get("timeStamp", 0)
    transitions.append({
        "name": "$initialise_machine",
        "params": None,
        "results": None,
        "destState": {
            "timeStamp": str(timestamp_scaled),
            "EGOposGT_X": str(ego_pos[0]) if ego_pos else "",
            "EGOposGT_Y": str(ego_pos[1]) if ego_pos else "",
            "EGOposGT_Z": str(ego_pos[2]) if ego_pos else "",
            "NPCposGT_X": str(npc_pos[0]) if npc_pos else "",
            "NPCposGT_Y": str(npc_pos[1]) if npc_pos else "",
            "NPCposGT_Z": str(npc_pos[2]) if npc_pos else "",
            "NPCposPerceived_X": str(perceived_pos[0]) if perceived_pos else "",
            "NPCposPerceived_Y": str(perceived_pos[1]) if perceived_pos else "",
            "NPCposPerceived_Z": str(perceived_pos[2]) if perceived_pos else "",
        },
        "destStateNotChanged": [],
        "preds": None
    })

    prev_timestamp = first_state.get("timeStamp", 0)
    prev_ego_pos = ego_pos
    prev_npc_pos = npc_pos
    prev_perceived_pos = perceived_pos

    #update till eof
    for state in states[1:]:
        curr_timestamp = state.get("timeStamp", 0)
        delta_time = curr_timestamp - prev_timestamp
        scaled_timestamp = curr_timestamp
        scaled_delta = delta_time

        ego_pos = extract_ego_position(state)
        npc_pos = extract_npc_position(state)
        perceived_pos = extract_npc_perceived(state)

        dest_state = {
            "timeStamp": str(scaled_timestamp),
            "EGOposGT_X": str(ego_pos[0]) if ego_pos else "",
            "EGOposGT_Y": str(ego_pos[1]) if ego_pos else "",
            "EGOposGT_Z": str(ego_pos[2]) if ego_pos else "",
            "NPCposGT_X": str(npc_pos[0]) if npc_pos else "",
            "NPCposGT_Y": str(npc_pos[1]) if npc_pos else "",
            "NPCposGT_Z": str(npc_pos[2]) if npc_pos else "",
            "NPCposPerceived_X": str(perceived_pos[0]) if perceived_pos else "",
            "NPCposPerceived_Y": str(perceived_pos[1]) if perceived_pos else "",
            "NPCposPerceived_Z": str(perceived_pos[2]) if perceived_pos else "",
        }

        dest_state_not_changed = []

        if ego_pos and prev_ego_pos:
            if ego_pos[0] == prev_ego_pos[0]:
                dest_state_not_changed.append("EGOposGT_X")
                dest_state.pop("EGOposGT_X", None)
            if ego_pos[1] == prev_ego_pos[1]:
                dest_state_not_changed.append("EGOposGT_Y")
                dest_state.pop("EGOposGT_Y", None)
            if ego_pos[2] == prev_ego_pos[2]:
                dest_state_not_changed.append("EGOposGT_Z")
                dest_state.pop("EGOposGT_Z", None)

        if npc_pos and prev_npc_pos:
            if npc_pos[0] == prev_npc_pos[0]:
                dest_state_not_changed.append("NPCposGT_X")
                dest_state.pop("NPCposGT_X", None)
            if npc_pos[1] == prev_npc_pos[1]:
                dest_state_not_changed.append("NPCposGT_Y")
                dest_state.pop("NPCposGT_Y", None)
            if npc_pos[2] == prev_npc_pos[2]:
                dest_state_not_changed.append("NPCposGT_Z")
                dest_state.pop("NPCposGT_Z", None)

        if perceived_pos and prev_perceived_pos:
            if perceived_pos[0] == prev_perceived_pos[0]:
                dest_state_not_changed.append("NPCposPerceived_X")
                dest_state.pop("NPCposPerceived_X", None)
            if perceived_pos[1] == prev_perceived_pos[1]:
                dest_state_not_changed.append("NPCposPerceived_Y")
                dest_state.pop("NPCposPerceived_Y", None)
            if perceived_pos[2] == prev_perceived_pos[2]:
                dest_state_not_changed.append("NPCposPerceived_Z")
                dest_state.pop("NPCposPerceived_Z", None)

        if ego_pos is None and prev_ego_pos is None:
            dest_state_not_changed.append("EGOposGT_X")
            dest_state_not_changed.append("EGOposGT_Y")
            dest_state_not_changed.append("EGOposGT_Z")
            dest_state.pop("EGOposGT_X", None)
            dest_state.pop("EGOposGT_Y", None)
            dest_state.pop("EGOposGT_Z", None)

        if npc_pos is None and prev_npc_pos is None:
            dest_state_not_changed.append("NPCposGT_X")
            dest_state_not_changed.append("NPCposGT_Y")
            dest_state_not_changed.append("NPCposGT_Z")
            dest_state.pop("NPCposGT_X", None)
            dest_state.pop("NPCposGT_Y", None)
            dest_state.pop("NPCposGT_Z", None)
        
        if perceived_pos is None and prev_perceived_pos is None:
            dest_state_not_changed.append("NPCposPerceived_X")
            dest_state_not_changed.append("NPCposPerceived_Y")
            dest_state_not_changed.append("NPCposPerceived_Z")
            dest_state.pop("NPCposPerceived_X", None)
            dest_state.pop("NPCposPerceived_Y", None)
            dest_state.pop("NPCposPerceived_Z", None)

        transition = {
            "name": "Update",
            "params": {
                "newTimeStamp": str(scaled_delta)
            },
            "results": {},
            "destState": dest_state,
            "destStateNotChanged": dest_state_not_changed,
            "preds": None
        }

        transitions.append(transition)
        prev_timestamp = curr_timestamp
        prev_npc_pos = npc_pos
        prev_perceived_pos = perceived_pos

    #structure
    output_data = {
        "description": "",
        "transitionList": transitions,
        "metadata": {
            "fileType": "Trace",
            "formatVersion": 1,
            "creator": "User",
            "proB2KernelVersion": "4.15.0-SNAPSHOT",
            "proBCliVersion": "1.15.0-final",
            "modelName": "AutoSimTraces"
        }
    }

    with open(output_file, 'w') as out_f:
        json.dump(output_data, out_f, indent=2)

    print(f"Converted {yaml_file} to {output_file}")



input_dir = Path("Input/")   
output_dir = Path("Output/") 

output_dir.mkdir(parents=True, exist_ok=True)  

for yaml_file in input_dir.glob("*.yaml"):
    output_file = output_dir / yaml_file.with_suffix(".prob2trace").name
    yaml_to_prob2trace_format(yaml_file, output_file)
