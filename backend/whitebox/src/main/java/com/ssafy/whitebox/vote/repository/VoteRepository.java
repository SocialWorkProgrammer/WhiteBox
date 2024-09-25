package com.ssafy.whitebox.vote.repository;

import com.ssafy.whitebox.ai.entity.AIResult;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import com.ssafy.whitebox.vote.entity.Vote;

@Repository
public interface VoteRepository extends JpaRepository<Vote, Long> {

    boolean existsByAiResult(AIResult aiResult);
}
