import { View, Text, StyleSheet } from 'react-native'
import React from 'react'
import { Link } from 'expo-router'

const register = () => {
  return (
    <div>
      <View style={styles.container}>
        <Text style={styles.text}>Register</Text>
      <input style={styles.midWidth} placeholder="email"/>
      <input style={styles.midWidth} placeholder="password" type="password"/>
      <button style={styles.midWidth}><Link href='/'>Already have an account</Link></button>
      <button style={styles.midWidth}><Link href='/'>Create</Link></button>
      </View>
    </div>
  )
}

export default register

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    flexDirection: 'column'
  },
  text: {
    color: 'white',
    fontSize: 42,
    fontWeight: 'bold',
    textAlign: 'center'
  },
  midWidth: {
    width: 200,
  }
})