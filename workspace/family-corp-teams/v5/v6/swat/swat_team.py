class SWATTeam:
    def __init__(self):
        self.incidents = {}
        self.next_incident_id = 1

    def dispatch(self, incident_type, details):
        incident_id = self.next_incident_id
        self.incidents[incident_id] = {
            'type': incident_type,
            'details': details,
            'status': 'pending'
        }
        self.next_incident_id += 1
        return incident_id

    def resolve(self, incident_id):
        if incident_id in self.incidents:
            self.incidents[incident_id]['status'] = 'resolved'
            return True
        return False

    def log(self, entry):
        print(f"[SWAT Log] {entry}")

    def status(self):
        return {incid: info['status'] for incid, info in self.incidents.items()}

# Example usage:
# swat = SWATTeam()
# incident_id = swat.dispatch("Emergency", "Critical system failure")
# print(f"Incident {incident_id} dispatched.")
# swat.resolve(incident_id)
# print("Status:", swat.status())