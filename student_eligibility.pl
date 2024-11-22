:- use_module(library(csv)).
:- use_module(library(http/http_server)).
:- use_module(library(http/http_parameters)).
:- use_module(library(http/http_json)). % Use this for reply_json/1

% Load CSV data as Prolog facts
load_csv_data :-
    csv_read_file("data.csv", Rows, [functor(student), arity(3)]),
    maplist(assert, Rows).

% Scholarship eligibility
eligible_for_scholarship(Student_ID) :-
    student(Student_ID, Attendance_Percentage, CGPA),
    Attendance_Percentage >= 75,
    CGPA >= 9.0.

permitted_for_exam(Student_ID) :-
    student(Student_ID, Attendance_Percentage, _),
    Attendance_Percentage >= 75.

% API to check scholarship eligibility
:- http_handler(root(scholarship), handle_scholarship_request, []).
:- http_handler(root(exam_permission), handle_exam_permission_request, []).

% Scholarship handler
handle_scholarship_request(Request) :-
    http_parameters(Request, [student_id(Student_ID, [integer])]),
    ( eligible_for_scholarship(Student_ID)
    -> Response = json{status: "eligible"}
    ; Response = json{status: "not eligible"}
    ),
    reply_json(Response).

handle_exam_permission_request(Request) :-
    % Use integer for student_id
    http_parameters(Request, [student_id(Student_ID, [integer])]),

    % Log received student_id for debugging
    format('Received student_id: ~w~n', [Student_ID]),

    % Check if the student is permitted for the exam
    ( permitted_for_exam(Student_ID)
    -> Response = json{status: "permitted"}
    ; Response = json{status: "not permitted"}
    ),

    % Send the response as JSON
    reply_json(Response).

% Start the server
start_server :-
    load_csv_data,
    http_server(http_dispatch, [port(8080)]).


