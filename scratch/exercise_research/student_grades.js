/*
Setup the exercise, load all relevant data and 
configure the cluster (if needed)
*/
function setup() {
	load('data/students.js');

	aClient = new HttpClient();
aClient.get('http://some/thing?with=arguments', function(response) {
    print(response);
});

	if (db.getSiblingDB("students").grades.count() == 5) {
		return true
	}
	else {
		print("Exercise was not successfully setup, cleaning up...");
		cleanup();
		return false;
	}
}

function getDescription() {
	return "Please add a grade field to each student, e.g. students >= 90 will get a grade of 'A', students
	 >= 80 < 90 will get a B, etc.";
}

/*
Solve the exercise, update any documents or configurations to 
pass the submit() function
*/
function solve()  {
	db.getSiblingDB("students").grades.update( { "grade" : { $gte : 90 } }, { $set : { "grade" : "A" } }, { "multi" : true });	
}

/*
Submit the exercise for correctness
*/
function submit() {
	if (db.getSiblingDB("students").grades.find( { "grade" : "A" }).count() == 1) {
		return true
	}
	else {
		print("Incorrect submission");
		return false;
	}
}

/*
Clean up the exercise, remove all inserted documents, indexes, etc.
*/
function cleanup() {
	print("Cleaning up...");
	db.getSiblingDB("students").grades.remove({});
}

// Run setup
setup();
