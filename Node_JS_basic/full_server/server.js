import express from 'express';
import router from './routes';

const app = express();
const PORT = 1245;

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(router);

app.listen(PORT, () => console.log(`Server running on port ${PORT}`));

export default app;
