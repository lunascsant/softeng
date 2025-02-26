import React, { useState } from 'react';
import {Text, TextInput, StyleSheet, TouchableOpacity, ScrollView } from 'react-native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { RootStackParamList } from '../App';
import { useNavigation } from '@react-navigation/native';

type RegisterScreenNavigationProp = NativeStackNavigationProp<RootStackParamList, 'Page1'>;

export default function RegisterScreen() {
  const navigation = useNavigation<RegisterScreenNavigationProp>();

  // State to handle form input values

  const [phone, setPhone] = useState('');

  const handleSubmit = () => {
    navigation.navigate('Home');
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>MoradiApp</Text>

      <Text style={styles.label}>E-mail</Text>
      <TextInput
        style={styles.input}
        placeholder="e-mail"
        keyboardType="email-address"
        value={phone}
        onChangeText={setPhone}
      />
    

      <TouchableOpacity style={styles.button} onPress={handleSubmit}>
        <Text style={styles.buttonText}>Redefinir senha</Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flexGrow: 1,
    justifyContent: 'flex-start',
    alignItems: 'center',
    backgroundColor: '#ffffff',
    paddingHorizontal: 20,
    paddingBottom: 20, // Adicionando espaço no final da tela para rolagem
  },
  icon: {
    marginRight: 10,
    marginTop: 12,
  },
  title: {
    fontSize: 60,
    color: '#2C3E50',
    marginBottom: 40,
    marginTop: 40,
  },
  input: {
    width: '100%',
    height: 50,
    borderColor: '#BDC3C7',
    borderWidth: 1,
    borderRadius: 25,
    marginBottom: 15,
    paddingLeft: 20,
    fontSize: 16,
  },
  forgotPassword: {
    textDecorationLine: 'underline', // Sublinhado
    fontSize: 16,
    marginTop: 30,
    alignSelf: 'flex-start', // Alinha à esquerda
  },
  fileButton: {
    backgroundColor: '#BDC3C7',
    height: 50,
    width: '100%',
    justifyContent: 'center',
    alignItems: 'center',
    borderRadius: 25,
    marginBottom: 15,
  },
  label: {
    alignSelf: 'flex-start',
    marginBottom: 5,
    color: '#2C3E50',
    fontSize: 16,
  },
  dropdown: {
    width: '100%',
    marginBottom: 15,
    height: 50,
  },
  dropdownInput: {
    backgroundColor: '#ffffff',
    borderWidth: 1,
    borderColor: '#BDC3C7',
    borderRadius: 25,
    paddingLeft: 20,
    fontSize: 16,
  },
  photoContainer: {
    width: '100%',
    marginBottom: 20,
    alignItems: 'center',
  },
  photoButton: {
    backgroundColor: '#F5A623',
    height: 50,
    width: '100%',
    justifyContent: 'center',
    alignItems: 'center',
    borderRadius: 25,
    marginBottom: 10,
  },
  photoPreview: {
    width: 100,
    height: 100,
    borderRadius: 50,
    marginTop: 10,
  },
  button: {
    backgroundColor: '#F5A623',
    height: 50,
    width: '100%',
    justifyContent: 'center',
    alignItems: 'center',
    borderRadius: 25,
    marginTop: 30,
  },
  buttonText: {
    color: '#ffffff',
    fontSize: 18,
    fontWeight: 'bold',
  },
});