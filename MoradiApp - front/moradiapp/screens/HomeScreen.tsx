import React from 'react';
import { View, Text, StyleSheet, Image, TouchableOpacity, ScrollView } from 'react-native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { useNavigation } from '@react-navigation/native';
import { RootStackParamList } from '../App';

type HomeScreenNavigationProp = NativeStackNavigationProp<RootStackParamList, 'Home'>;

export default function HomeScreen() {
  const navigation = useNavigation<HomeScreenNavigationProp>();

  const handleSubmit = () => {
    navigation.navigate('Page4');
  };

  const handleSubmit2 = () => {
    navigation.navigate('Page6');
  };

  const handleSubmit3 = () => {
    navigation.navigate('Page8');
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>MoradiApp</Text>
      <Image source={require('../assets/homeScreen.jpg')} style={styles.image} />
      <View style={styles.buttonContainer}>
        <TouchableOpacity
          style={[styles.button, styles.registerButton]}
          onPress={() => navigation.navigate('Page1')}
        >
          <Text style={styles.buttonText}>Registrar-se</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.button, styles.loginButton]}
          onPress={() => navigation.navigate('Page2')}
        >
          <Text style={styles.buttonText}>Entrar</Text>
        </TouchableOpacity>

        <TouchableOpacity style={[styles.button, styles.loginButton]} onPress={handleSubmit}>
          <Text style={styles.buttonText}>Navegar fluxo Adm</Text>
        </TouchableOpacity>

        <TouchableOpacity style={[styles.button, styles.loginButton]} onPress={handleSubmit2}>
          <Text style={styles.buttonText}>Navegar fluxo Padrão</Text>
        </TouchableOpacity>

        <TouchableOpacity style={[styles.button, styles.loginButton]} onPress={handleSubmit3}>
          <Text style={styles.buttonText}>Navegar fluxo Convidado</Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flexGrow: 1, // Para garantir que o ScrollView ocupe o máximo de espaço possível
    justifyContent: 'flex-start',
    alignItems: 'center',
    backgroundColor: '#ffffff',
    paddingHorizontal: 20,
    paddingBottom: 30, // Adicionando um pequeno padding na parte inferior
  },
  title: {
    fontSize: 60,
    color: '#2C3E50',
    marginBottom: 40,
    marginTop: 40,
  },
  image: {
    width: 300,
    height: 300,
    marginBottom: 30,
  },
  buttonContainer: {
    width: '100%',
    marginTop: 30,
    paddingHorizontal: 20,
  },
  forgotPassword: {
    textDecorationLine: 'underline', // Sublinhado
    fontSize: 16,
    marginTop: 30,
    alignSelf: 'flex-start', // Alinha à esquerda
    color: '#000000',
  },
  button: {
    height: 50,
    borderRadius: 25,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 15,
  },
  registerButton: {
    backgroundColor: '#F5A623', // Amarelo
  },
  loginButton: {
    backgroundColor: '#F5A623', // Amarelo
  },
  buttonText: {
    color: '#ffffff', // Texto branco
    fontSize: 18,
    fontWeight: 'bold',
  },
});
