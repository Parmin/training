function setup() {
	load('data/students.js');

	if (db.getSiblingDB("students").grades.count() == 5) {
		return true
	}
	else {
		print("Exercise was not successfully setup, cleaning up...");
		cleanup();
		return false;
	}
}

function solve()  {
	db.getSiblingDB("students").grades.find( { "grade" : "A" })	
}

function submit() {
	if (db.getSiblingDB("students").grades.find( { "grade" : "A" }) == 1) {
		return true
	}
	else {
		print("Incorrect submission");
		return false;
	}

}

function cleanup() {
	print("Cleaning up...");
	db.getSiblingDB("students").grades.remove({});
}

setup();
