import { View, Text, StyleSheet } from 'react-native'
import React from 'react'
import { Link } from 'expo-router'

const logged = () => {
  return (
    <div>
      <View style={styles.container}>
        <Text style={styles.text}>Welcome ! you are logged in</Text>
      </View>
    </div>
  )
}

export default logged

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
  }
})