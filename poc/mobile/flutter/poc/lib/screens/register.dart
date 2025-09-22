import 'package:flutter/material.dart';
import 'login.dart';

class RegisterPage extends StatefulWidget {
  @override
  State<RegisterPage> createState() => _RegisterPageState();
}


class _RegisterPageState extends State<RegisterPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SingleChildScrollView(
        child: Column(
          children: <Widget>[
            Padding(
              padding: const EdgeInsets.only(top: 110.0),
              child: Center(
                  child: Text(
                    'Register Page',
                    style: TextStyle(color: Colors.red, fontSize: 20),
                ),
              ),
            ),
            Padding(
              padding: EdgeInsets.only(top: 15),
              child: TextField(
                decoration: InputDecoration(
                  border: OutlineInputBorder(),
                  labelText: 'Email',
                ),
              ),
            ),
            Padding(
              padding: const EdgeInsets.only(top: 15),
              child: TextField(
                decoration: InputDecoration(
                  border: OutlineInputBorder(),
                  labelText: 'Password',
                ),
              ),
            ),

            SizedBox(
              height: 65,
              width: 300,
              child: Padding(
                padding: const EdgeInsets.only(top: 20.0),
                child: ElevatedButton(
                  child: Text(
                    'Register',
                    style: TextStyle(color: Colors.red, fontSize: 20),
                  ),
                  onPressed: () {
                    print('Successfully register');
                  },
                ),
              ),
            ),

            SizedBox(
              height: 65,
              width: 300,
              child: Padding(
                padding: const EdgeInsets.only(top: 20.0),
                child: ElevatedButton(
                  child: Text(
                    'Login',
                    style: TextStyle(color: Colors.red, fontSize: 20),
                  ),
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(builder: (context) => LoginPage()),
                    );                  },
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
