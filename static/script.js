// ========================================
// STUDENT MANAGEMENT SYSTEM
// JAVASCRIPT
// ========================================


// ========================================
// LOAD STUDENTS WHEN PAGE OPENS
// ========================================

window.onload = function () {
    loadStudents();
};


// ========================================
// LOAD ALL STUDENTS
// ========================================

function loadStudents() {

    fetch("/students")

        .then(response => response.json())

        .then(data => {

            // Update dashboard student count
            document.getElementById("totalStudents").textContent = data.length;

            // Display student records
            displayStudents(data);

        });
}


// ========================================
// DISPLAY STUDENTS IN TABLE
// ========================================

function displayStudents(students) {

    let table = document.getElementById("studentTable");

    table.innerHTML = "";


    // If no students found
    if (students.length === 0) {

        table.innerHTML = `
            <tr>
                <td colspan="7">
                    No student records found
                </td>
            </tr>
        `;

        return;
    }


    // Display every student
    students.forEach(student => {

        table.innerHTML += `

            <tr>

                <td>${student.id}</td>

                <td>${student.name}</td>

                <td>${student.roll_no}</td>

                <td>${student.class_name}</td>

                <td>${student.marks}</td>

                <td>${student.contact}</td>

                <td>

                    <button
                        onclick='editStudent(${JSON.stringify(student)})'>
                        ✏️ Edit
                    </button>

                    <button
                        onclick="deleteStudent(${student.id})">
                        🗑️ Delete
                    </button>

                </td>

            </tr>

        `;
    });
}


// ========================================
// ADD / UPDATE STUDENT
// ========================================

function saveStudent() {

    let id = document.getElementById("studentId").value;


    // Collect student information
    let student = {

        name: document.getElementById("name").value,

        roll_no: document.getElementById("roll_no").value,

        class_name: document.getElementById("class_name").value,

        marks: document.getElementById("marks").value,

        contact: document.getElementById("contact").value

    };


    // Default: Add student
    let url = "/students";

    let method = "POST";


    // If ID exists → Update student
    if (id) {

        url = "/students/" + id;

        method = "PUT";

    }


    fetch(url, {

        method: method,

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(student)

    })


    .then(response => response.json())


    .then(data => {

        alert(data.message || data.error);


        // If operation successful
        if (!data.error) {

            clearForm();

            loadStudents();

        }

    });

}


// ========================================
// EDIT STUDENT
// ========================================

function editStudent(student) {

    document.getElementById("studentId").value = student.id;

    document.getElementById("name").value = student.name;

    document.getElementById("roll_no").value = student.roll_no;

    document.getElementById("class_name").value = student.class_name;

    document.getElementById("marks").value = student.marks;

    document.getElementById("contact").value = student.contact;


    // Scroll to form
    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });

}


// ========================================
// DELETE STUDENT
// ========================================

function deleteStudent(id) {

    if (!confirm("Are you sure you want to delete this student?")) {
        return;
    }


    fetch("/students/" + id, {

        method: "DELETE"

    })


    .then(response => response.json())


    .then(data => {

        alert(data.message || data.error);

        loadStudents();

    });

}


// ========================================
// SEARCH STUDENT
// ========================================

function searchStudent() {

    let name = document.getElementById("searchName").value.trim();

    let roll = document.getElementById("searchRoll").value.trim();


    let url = "/students/search?";


    // Search by name
    if (name) {

        url += "name=" + encodeURIComponent(name);

    }


    // Otherwise search by roll number
    else if (roll) {

        url += "roll_no=" + encodeURIComponent(roll);

    }


    fetch(url)

        .then(response => response.json())

        .then(data => {

            displayStudents(data);

        });

}


// ========================================
// CLEAR FORM
// ========================================

function clearForm() {

    document.getElementById("studentId").value = "";

    document.getElementById("name").value = "";

    document.getElementById("roll_no").value = "";

    document.getElementById("class_name").value = "";

    document.getElementById("marks").value = "";

    document.getElementById("contact").value = "";

}