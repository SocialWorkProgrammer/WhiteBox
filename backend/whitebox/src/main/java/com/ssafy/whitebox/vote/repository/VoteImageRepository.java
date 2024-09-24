package com.ssafy.whitebox.vote.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import com.ssafy.whitebox.vote.entity.VoteImage;

@Repository
public interface VoteImageRepository extends JpaRepository<VoteImage, Long> {
}
