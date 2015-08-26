module.exports = function(grunt) {
  require("matchdep").filterDev("grunt-*").forEach(grunt.loadNpmTasks);

  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    concat: {
      options: {
        separator: ';'
      },
      dist: {
        src: ['app/js/*.js'],
        dest: 'app/js/dist/<%= pkg.name %>.js'
      }
    },
    ngAnnotate: {
      options: {
        singleQuotes: true,
      },
      dist: {
        src: ['<%= concat.dist.dest %>'],
        dest: 'app/js/dist/<%= pkg.name %>.annotate.js'
      }
    },
    uglify: {
      options: {
        banner: '/*! <%= pkg.name %> <%= grunt.template.today("dd-mm-yyyy") %> */\n',
        mangle: false,
        compress: {} // use default compress options
      },
      dist: {
        files: {
          'app/js/dist/<%= pkg.name %>.min.js': ['<%= ngAnnotate.dist.dest %>']
        }
      }
    },
    htmlhint: {
      options: {
          'tag-pair': true,
          'tagname-lowercase': true,
          'attr-lowercase': true,
          'attr-value-double-quotes': true,
          //'doctype-first': true,
          'spec-char-escape': true,
          'id-unique': true,
          //'style-disabled': true,
          'head-script-disabled': true
      },
      files: ['app/index.html', 'app/partials/**/*.html']
    },
    jshint: {
      files: ['Gruntfile.js', 'app/js/*.js'],
      options: {
        jshintrc: '.jshintrc',
        globals: {
          jQuery: true,
          console: true,
          module: true
        }
      }
    },
    qunit: {
      files: ['app/index.html', 'app/partials/**/*.html']
    },
    watch: {
      files: ['<%= jshint.files %>'],
      tasks: ['jshint']
    }
  });

  grunt.registerTask('test', ['htmlhint', 'jshint']);
  grunt.registerTask('default', ['concat','ngAnnotate','uglify']);

};
