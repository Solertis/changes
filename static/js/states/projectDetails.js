define([
  'app'
], function(app) {
  'use strict';

  return {
    abstract: true,
    parent: 'projects',
    url: ':project_id/',
    templateUrl: 'partials/project-details.html',
    controller: function($scope, $rootScope, projectData) {
      $scope.project = projectData;
      $rootScope.activeProject = $scope.project;
      $rootScope.pageTitle = projectData.name;
    },
    resolve: {
      projectData: function($http, $location, $stateParams) {
        return $http.get('/api/0/projects/' + $stateParams.project_id + '/').error(function(){
          $location.path('/');
        }).then(function(response){
          return response.data;
        });
      }
    }
  };
});
