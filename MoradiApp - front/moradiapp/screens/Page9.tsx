import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView } from 'react-native';
import { useNavigation } from '@react-navigation/native';

export default function HomeScreen() {
  const navigation = useNavigation(); // Hook de navegação

  return (
    <View style={styles.container}>
      <Text style={styles.subtitle}>Moradia 01</Text>
      <TouchableOpacity style={styles.createGroupButton}>
        <Text style={styles.createGroupButtonText}>Acessar normas de convivência</Text>
      </TouchableOpacity>

    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F2F6F7',
    paddingHorizontal: 20,
    paddingTop: 40,
  },
  subtitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#2C3E50',
    marginBottom: 20,
  },
  listContainer: {
    flex: 1,
  },
  moradiaCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: 10,
    padding: 15,
    marginBottom: 15,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 5,
  },
  cardHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 10,
  },
  moradiaTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginLeft: 10,
    color: '#2C3E50',
  },
  cardText: {
    fontSize: 14,
    color: '#7F8C8D',
    marginBottom: 5,
  },
  createGroupButton: {
    backgroundColor: '#2C3E50',
    borderRadius: 25,
    paddingVertical: 15,
    alignItems: 'center',
    marginTop: 5,
    marginBottom: 10,
  },
  createGroupButtonText: {
    fontSize: 17,
    color: '#FFFFFF',
    fontWeight: 'bold',
  },
});
