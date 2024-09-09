package com.ssafy.whitebox.user.entity;

import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface UserRepository extends JpaRepository<User, Long> {

    Optional<User> findByUserEmail(String userEmail);

    boolean existsByUserNickname(String userNickname);

    boolean existsByUserEmail(String userEmail);
}
