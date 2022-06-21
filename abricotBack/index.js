const express = require('express');
const dotenv = require('dotenv');
const multer = require('multer');
const upload = multer({dest: 'uploads/'});
const cors = require('cors');
const app = express();
const fs = require('fs');
var { PythonShell } = require('python-shell');
const tarfs = require('tar-fs');
const {
    untarFile
} = require('./unpack');

var type = upload.single('file');

dotenv.config();

app.use((req, res, next) => {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content, Accept, Content-Type, Authorization, X-Auth-Token');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, PATCH, OPTIONS');
    if (req.method === 'OPTIONS')
        res.sendStatus(200);
    else
        next();
});

app.use(express.json());

const getRandomName = () => {
    return Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
}


app.post('/check-norme', type, (req, res, next) => {
    if (req.file === undefined || req.file.path === undefined)
        return res.status(400).send({
            "msg" : "Bad request"
        })
    var randomName = getRandomName();
    var options = {
        mode: 'text',
        pythonPath: '/usr/bin/python3',
        pythonOptions: ['-u'],
        scriptPath: './',
        args: ['--dir', 'uploads/' + randomName]
    };
    fs.createReadStream(req.file.path).pipe(tarfs.extract('./uploads/' + randomName))
    .on('finish', () => PythonShell.run('brico.py', options, (err, results) => {
        if (err) throw err;
        fs.rmdir('./uploads/' + randomName, {recursive: true}, (err) => {});
        fs.rm(req.file.path, {recursive: true}, (err) => {});
        res.send(results);
    }));
});

app.listen(process.env.PORT || 3589, () => {
    console.log(`Server running boi on port ${process.env.PORT || 3589}`);
})
