---
layout: default
title: Arquivos PD Processados
---

<h2>Arquivos PD disponíveis:</h2>

<ul>
{% for file_name in site.data %}
    {% assign file_data = file_name %}
    {% if file_data %}
        <li>
            <strong>Nome do Arquivo:</strong> {{ file_name[1].filename }}<br>
            <br>
            <ul>
            {% for obj in file_data[1].objects %}
                <li>
                    <strong>Tipo:</strong> {{ obj.type }}<br>
                    <strong>Parâmetros:</strong> {{ obj.parameters }}<br>
                    <strong>Posição X:</strong> {{ obj.X }}<br>
                    <strong>Posição Y:</strong> {{ obj.Y }}<br>
                    {% if obj.type == "route" %}
                        <strong>Plug 0:</strong> {{ obj.plug_0 }}<br>
                        <strong>Plug 1:</strong> {{ obj.plug_1 }}<br>
                        <strong>Plug 2:</strong> {{ obj.plug_2 }}<br>
                        <strong>Plug 3:</strong> {{ obj.plug_3 }}<br>
                        <strong>Plug 4:</strong> {{ obj.plug_4 }}<br>                        
                    {% endif %}
                    <br>
                </li>
            {% endfor %}
            </ul>
        </li>
    {% else %}
        <li>Dados para {{ file_name }} não encontrados.</li>
    {% endif %}
{% endfor %}
</ul>
