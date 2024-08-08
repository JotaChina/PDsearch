document.addEventListener('DOMContentLoaded', function() {
    // Carregar JSON files
    async function loadJSONFiles() {
      const response = await fetch('{{ '/data/instruments.json' | relative_url }}');
      return response.json();
    }
  
    function indexInstruments(data) {
      const instrumentProjects = {};
      data.forEach(project => {
        const filename = project.filename;
        project.objects.forEach(obj => {
          const instrumentType = obj.type;
          if (instrumentType === 'route') {
            const routeParameters = obj.parameters.split(' ');
            routeParameters.forEach(param => {
              if (!instrumentProjects[param]) {
                instrumentProjects[param] = {};
              }
              if (!instrumentProjects[param][filename]) {
                instrumentProjects[param][filename] = [];
              }
              instrumentProjects[param][filename].push(obj);
            });
          } else {
            if (!instrumentProjects[instrumentType]) {
              instrumentProjects[instrumentType] = {};
            }
            if (!instrumentProjects[instrumentType][filename]) {
              instrumentProjects[instrumentType][filename] = [];
            }
            instrumentProjects[instrumentType][filename].push(obj);
          }
        });
      });
      return instrumentProjects;
    }
  
    function searchInstruments(instrumentProjects, searchTerm) {
      const results = {};
      const searchParts = searchTerm.split(' ');
  
      if (searchParts.length === 0) return results;
  
      const searchType = searchParts[0];
      const searchParams = searchParts.slice(1).join(' ').trim();
  
      for (const [instrument, projects] of Object.entries(instrumentProjects)) {
        if (searchType === "route") {
          for (const [project, configs] of Object.entries(projects)) {
            configs.forEach(config => {
              if (config.type === "route") {
                if (!results[instrument]) {
                  results[instrument] = {};
                }
                if (!results[instrument][project]) {
                  results[instrument][project] = [];
                }
                results[instrument][project].push(config);
              }
            });
          }
        } else if (searchType === instrument || searchParams === instrument) {
          for (const [project, configs] of Object.entries(projects)) {
            configs.forEach(config => {
              if (config.parameters.includes(searchParams)) {
                if (!results[instrument]) {
                  results[instrument] = {};
                }
                if (!results[instrument][project]) {
                  results[instrument][project] = [];
                }
                results[instrument][project].push(config);
              }
            });
          }
        }
      }
      return results;
    }
  
    document.getElementById('search-form').addEventListener('submit', async function(event) {
      event.preventDefault();
      const searchTerm = document.getElementById('search-input').value.trim();
      const data = await loadJSONFiles();
      const instrumentProjects = indexInstruments(data);
      const results = searchInstruments(instrumentProjects, searchTerm);
      displayResults(results);
    });
  
    function displayResults(results) {
      const resultsDiv = document.getElementById('results');
      resultsDiv.innerHTML = '';
      if (Object.keys(results).length === 0) {
        resultsDiv.innerHTML = '<p>Nenhum projeto encontrado com o termo de busca fornecido.</p>';
        return;
      }
  
      for (const [instrument, projects] of Object.entries(results)) {
        const instrumentDiv = document.createElement('div');
        instrumentDiv.innerHTML = `<h2>Tipo: ${instrument}</h2>`;
        for (const [project, configs] of Object.entries(projects)) {
          const projectDiv = document.createElement('div');
          projectDiv.innerHTML = `<h3>Projeto: ${project}</h3>`;
          configs.forEach(config => {
            projectDiv.innerHTML += `<p>${config.type} X: ${config.X} Y: ${config.Y}</p>`;
          });
          instrumentDiv.appendChild(projectDiv);
        }
        resultsDiv.appendChild(instrumentDiv);
      }
    }
  });
  