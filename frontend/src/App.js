import './App.css';

import { useEffect, useState } from 'react';
import Axios from 'axios';


const updateUserData = (setUserData) => {
    Axios({
        url: "/api/user",
        method: "GET",
    }).then(r => {
        // console.log('r.data', JSON.stringify(r.data));
        setUserData(r.data);
    })
};

const deleteUser = (e, setUserData) => {
    // console.log('e.target.id', e.target.id);
    const uud = () => updateUserData(setUserData);
    Axios({
        url: '/api/user',
        method: 'DELETE',
        data: {
            user_id: e.target.id,
        }
    }).then(uud)
};

const User = ({user, setUserData}) => {
    // console.log("user", user)
    return (
        <tr>
            <td>
                <input type="button" value="Delete" onClick={e => deleteUser(e, setUserData)} id={user.user_id} />
            </td>
            <td>{user.user_id}</td>
            <td>{user.username}</td>
        </tr>
    );
};

const Users = ({userData, setUserData}) => {
    // console.log('userData', JSON.stringify(userData))
    return (
        <table>
            <tbody>
                <tr>
                    <th>Actions</th>
                    <th>UserId</th>
                    <th>Username</th>
                </tr>
                {userData.map(u => <User user={u} setUserData={setUserData} key={u.user_id} />)}
            </tbody>
        </table>
    );
};

function App() {
    const [userData, setUserData] = useState([]);

    useEffect(() => {
        updateUserData(setUserData);
    }, [setUserData])

    const newUserHandler = (e) => {
        e.preventDefault();
        Axios({
            url: "/api/user",
            method: "PUT",
            data: {
                username: document.getElementById("new_username").value,
            },
        }).then(r => {
            // console.log('r.data', JSON.stringify(r.data));
            updateUserData(setUserData);
        })
    };

    return (
        <div className="App">
            <header className="App-header">
                <form onSubmit={newUserHandler}>
                    <input id="new_username" type="text" name="username" />
                    <input type="submit" value="Create New User" onSubmit={newUserHandler} />
                </form>

                <Users userData={userData} setUserData={setUserData}/>
            </header>
        </div>
    );
}

export default App;
