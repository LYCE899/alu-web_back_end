import express from 'express';
import AppController from '../controllers/AppController';
import StudentsController from '../controllers/StudentsController';

/*
Link the route / to the AppController
Link the route /students and /students/:major to the StudentsController
 */

const router = express.Router();

router.get('/', AppController.getHomePage);
router.get('/students', StudentsController.getAllStudents);
router.get('/students/:major', StudentsController.getAllStudentsByMajor);

export default router;
