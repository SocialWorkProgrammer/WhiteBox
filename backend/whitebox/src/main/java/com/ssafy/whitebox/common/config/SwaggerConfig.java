package com.ssafy.whitebox.common.config;


import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Info;
import org.springdoc.core.models.GroupedOpenApi;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class SwaggerConfig {

    @Bean
    public OpenAPI openAPI() {
        return new OpenAPI()
                .info(new Info()
                        .title("WhiteBox-OpenAPI")
                        .version("1.0")
                        .description("WhiteBox에서 제공하는 API를 확인하세요"));
    }

    @Bean
    public GroupedOpenApi api() {
        String [] paths = {"/api/**"};
        String [] packagesToScan = {"com.ssafy.whitebox"};
        return GroupedOpenApi.builder().group("springDoc-openAPI")
                .pathsToMatch(paths)
                .packagesToScan(packagesToScan)
                .build();
    }
}
