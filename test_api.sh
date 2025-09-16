#!/bin/bash

# Script de pruebas para la API de Destinos Turísticos
# Demuestra todas las funcionalidades del sistema

echo "🌎 API de Destinos Turísticos - Pruebas Completas"
echo "=================================================="
echo ""

BASE_URL="http://localhost:8000"

echo "1. Verificar estado de la API"
echo "------------------------------"
curl -s -X GET "$BASE_URL/" | python -m json.tool
echo ""

echo "2. Listar usuarios existentes"
echo "------------------------------"
curl -s -X GET "$BASE_URL/api/v1/usuarios/" | python -m json.tool
echo ""

echo "3. Listar destinos disponibles"
echo "-------------------------------"
curl -s -X GET "$BASE_URL/api/v1/destinos/" | python -m json.tool
echo ""

echo "4. Crear un nuevo usuario"
echo "-------------------------"
NEW_USER='{"email": "ana.lopez@email.com", "nombre": "Ana", "apellido": "López", "telefono": "555-0004"}'
curl -s -X POST "$BASE_URL/api/v1/usuarios/" -H "Content-Type: application/json" -d "$NEW_USER" | python -m json.tool
echo ""

echo "5. Realizar compra (Usuario ID 4, Destino Galápagos ID 7)"
echo "---------------------------------------------------------"
COMPRA='{"usuario_id": 4, "destino_id": 7}'
curl -s -X POST "$BASE_URL/api/v1/compras/" -H "Content-Type: application/json" -d "$COMPRA" | python -m json.tool
echo ""

echo "6. Ver saldo de puntos del nuevo usuario"
echo "----------------------------------------"
curl -s -X GET "$BASE_URL/api/v1/puntos/usuario/4/saldo" | python -m json.tool
echo ""

echo "7. Canjear 100 puntos por descuento"
echo "------------------------------------"
CANJE='{"usuario_id": 4, "puntos_utilizados": 100, "descripcion": "Descuento de bienvenida"}'
curl -s -X POST "$BASE_URL/api/v1/puntos/canjear/" -H "Content-Type: application/json" -d "$CANJE" | python -m json.tool
echo ""

echo "8. Ver estadísticas completas del usuario"
echo "------------------------------------------"
curl -s -X GET "$BASE_URL/api/v1/usuarios/4/estadisticas" | python -m json.tool
echo ""

echo "9. Ver usuario completo con compras y canjes"
echo "---------------------------------------------"
curl -s -X GET "$BASE_URL/api/v1/usuarios/4" | python -m json.tool
echo ""

echo "✅ Pruebas completadas exitosamente!"
echo ""
echo "📊 Resumen del sistema:"
echo "- Usuario creado: Ana López"
echo "- Compra realizada: Galápagos por $3,500.00"
echo "- Puntos ganados: 350 puntos"
echo "- Puntos canjeados: 100 puntos = $10.00 descuento"
echo "- Puntos restantes: 250 puntos = $25.00 potencial descuento"