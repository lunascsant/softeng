import React, { useState } from 'react';
import { View, Text, TextInput, StyleSheet, TouchableOpacity, ScrollView } from 'react-native';
import { MaterialIcons } from 'react-native-vector-icons';
import DropDownPicker from 'react-native-dropdown-picker';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { RootStackParamList } from '../App';
import { useNavigation } from '@react-navigation/native';

type RegisterScreenNavigationProp = NativeStackNavigationProp<RootStackParamList, 'Page1'>;

export default function RegisterScreen() {
  const navigation = useNavigation<RegisterScreenNavigationProp>();

  // State to handle form input values
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [password, setPassword] = useState('');
  const [userType, setUserType] = useState('Administrador');
  const [photo, setPhoto] = useState('');

  // State to control dropdown visibility
  const [open, setOpen] = useState(false);

  const [fileName, setFileName] = useState('');
  const handleFileSelect = () => {
    // Simulate selecting a file (e.g., image)
    setFileName('Arquivo selecionado: imagem.jpg'); // Nome fictício do arquivo
  };

  const handleSubmit = () => {
    // Handle form submission logic here
    navigation.navigate('Home');
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>MoradiApp</Text>
      <Text style={styles.label}>Nome</Text>
      <TextInput
        style={styles.input}
        placeholder="Nome"
        value={name}
        onChangeText={setName}
      />
      <Text style={styles.label}>E-mail</Text>
      <TextInput
        style={styles.input}
        placeholder="E-mail"
        keyboardType="email-address"
        value={email}
        onChangeText={setEmail}
      />
      <Text style={styles.label}>Telefone (DDD + Número)</Text>
      <TextInput
        style={styles.input}
        placeholder="Telefone (DDD + número)"
        keyboardType="phone-pad"
        value={phone}
        onChangeText={setPhone}
      />
      <Text style={styles.label}>Senha</Text>
      <TextInput
        style={styles.input}
        placeholder="Senha"
        secureTextEntry
        value={password}
        onChangeText={setPassword}
      />

      {/* Dropdown for Tipo de usuário */}
      <Text style={styles.label}>Tipo de usuário</Text>
      <DropDownPicker
        open={open}
        value={userType}
        items={[
          { label: 'Administrador', value: 'Administrador' },
          { label: 'Morador Padrão', value: 'Morador Padrão' },
          { label: 'Morador Convidado', value: 'Morador Convidado' },
        ]}
        setOpen={setOpen} 
        setValue={setUserType}
        containerStyle={styles.dropdown}
        style={styles.dropdownInput} 
        placeholder="Selecione um tipo"
      />

      <Text style={styles.label}>Foto</Text>
      <TouchableOpacity style={styles.input} onPress={handleFileSelect}>
        <MaterialIcons name="attach-file" size={24} style={styles.icon} />
      </TouchableOpacity>

      <TouchableOpacity style={styles.button} onPress={handleSubmit}>
        <Text style={styles.buttonText}>Registrar-se</Text>
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