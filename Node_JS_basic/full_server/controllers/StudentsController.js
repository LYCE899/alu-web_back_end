import readDatabase from '../utils';

export default class StudentsController {
  /* The first one is getAllStudents:
  The method accepts request and response as argument
  It should return a status 200
  It calls the function readDatabase from the utils file, and display in the page:
  First line: This is the list of our students And for each field
  (order by alphabetic order case insensitive),
  a line that displays the number of students in the field, and the list of first names
  (ordered by appearance in the database file) with the following format:
  Number of students in FIELD: 6. List: LIST_OF_FIRSTNAMES If the database is not available,
   it should return a status 500 and the error message Cannot load the database
*/

  static async getAllStudents(req, res) {
    try {
      const path = process.argv[2];
      const data = await readDatabase(path);

      let returnData = 'This is the list of our students\n';
      const lines = data
        .toString()
        .split('\n')
        .filter((line) => line.length > 0)
        .slice(1);
      const fields = lines.map((line) => line.split(','));
      const fieldNames = fields.map((field) => field[3]).flat();
      const uniqueFieldNames = [...new Set(fieldNames)];
      uniqueFieldNames.forEach((field, index) => {
        const students = fields.filter((student) => student[3] === field);
        const studentNames = students.map((student) => student[0]);
        if (index === uniqueFieldNames.length - 1) {
          returnData += `Number of students in ${field}: ${
            students.length
          }. List : ${studentNames.join(', ')}`;
          return;
        }
        returnData += `Number of students in ${field}: ${
          students.length
        }. List : ${studentNames.join(', ')}\n`;
      });
      return res.status(200).send(returnData);
    } catch (error) {
      return res.status(500).send('Cannot load the database');
    }
  }
  /* The second one is getAllStudentsByMajor:
  The method accepts request and response as argument.
  It should return a status 200.
  It uses a parameter that the user can pass to the browser major.
  The major can only be CS or SWE. If the user is passing another parameter,
  the server should return a 500 and the error Major parameter must be CS or SWE.

  It calls the function readDatabase from the utils file,
  and display in the page the list of first names for the students
  (ordered by appearance in the database file) in the specified field
  List: LIST_OF_FIRSTNAMES_IN_THE_FIELD
  If the database is not available, it should return a status 500 and the error message
  Cannot load the database
*/

  static async getAllStudentsByMajor(req, res) {
    const { major } = req.params;
    if (major !== 'CS' && major !== 'SWE') {
      return res.status(500).send('Major parameter must be CS or SWE');
    }
    try {
      const path = process.argv[2];
      const data = await readDatabase(path);
      const lines = data
        .toString()
        .split('\n')
        .filter((line) => line.length > 0)
        .slice(1);
      const majorStudents = lines.filter((line) => line.length > 0).slice(1);
      const students = majorStudents.map((student) => student.split(',')[0]);
      const returnData = `List: ${students.join(', ')}`;
      return res.status(200).end(returnData);
    } catch (error) {
      return res.status(500).send('Cannot load the database');
    }
  }
}
